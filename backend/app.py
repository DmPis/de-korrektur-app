from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import uuid

from ocr import OCR
from grammar import GrammarChecker
from postproc import build_explanations
from exporter import export_docx

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DE PDF→Text Korrektur API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATA = Path("/app/data")
DATA.mkdir(parents=True, exist_ok=True)

class ProcessResult(BaseModel):
    job_id: str
    pages: list[str]
    clean_text: str
    marked_html: str
    explanations: list[dict]
    stats: dict

@app.post("/process", response_model=ProcessResult)
async def process_pdf(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    job_dir = DATA / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = job_dir / file.filename
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    ocr = OCR(job_dir)
    imgs = ocr.pdf_to_images(pdf_path, dpi=400)

    page_texts = []
    for p in imgs:
        t = ocr.image_to_text(p, lang="deu", psm=6)
        page_texts.append(ocr.clean_text(t))

    clean_text = "\n\n".join([f"=== Seite {i+1} ===\n" + tx for i, tx in enumerate(page_texts)])

    checker = GrammarChecker()
    errors = checker.check(clean_text)
    marked_html = checker.apply_markers(clean_text, errors)

    explanations = build_explanations(errors)
    stats = checker.stats(errors)

    # Export DOCX
    docx_path = job_dir / "result.docx"
    export_docx(clean_text, marked_html, docx_path)

    return JSONResponse(ProcessResult(
        job_id=job_id,
        pages=page_texts,
        clean_text=clean_text,
        marked_html=marked_html,
        explanations=explanations,
        stats=stats
    ).model_dump())

@app.get("/export/docx/{job_id}")
async def get_docx(job_id: str):
    path = DATA / job_id / "result.docx"
    if not path.exists():
        return JSONResponse({"error": "not_found"}, status_code=404)
    return FileResponse(path, filename=f"de-korrektur-{job_id}.docx")
