from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from pathlib import Path
import re

class OCR:
    def __init__(self, workdir: Path):
        self.workdir = workdir
        self.workdir.mkdir(parents=True, exist_ok=True)

    def _preprocess(self, img: Image.Image) -> Image.Image:
        g = img.convert("L")
        g = ImageOps.autocontrast(g)
        g = g.filter(ImageFilter.MedianFilter(size=3))
        return g

    def pdf_to_images(self, pdf_path: Path, dpi: int = 400) -> list[Path]:
        pages = convert_from_path(str(pdf_path), dpi=dpi)
        out = []
        for i, p in enumerate(pages, 1):
            pth = self.workdir / f"page_{i:03d}.png"
            p.save(pth)
            out.append(pth)
        return out

    def image_to_text(self, image_path: Path, lang: str = "deu", psm: int = 6) -> str:
        cfg = f"--oem 1 --psm {psm}"
        img = Image.open(image_path)
        img = self._preprocess(img)
        text = pytesseract.image_to_string(img, lang=lang, config=cfg)
        return text

    @staticmethod
    def clean_text(t: str) -> str:
        t = t.replace("\r", "")
        t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)  # join hyphenated linebreaks
        t = re.sub(r"\n{3,}", "\n\n", t)
        t = t.strip()
        return t
