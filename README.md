# DE PDF→Text Korrektur (German OCR + Grammar)

Полностью автономное приложение: принимает PDF (немецкий, печатный/рукописный), конвертирует страницы в изображения, делает OCR (Tesseract **deu**), проверяет грамматику (LanguageTool), подсвечивает ошибки и экспортирует DOCX.

## Быстрый старт

```bash
git clone <this-repo>
cd de-korrektur-app
docker compose up --build
# API: http://localhost:8080
# LanguageTool: http://localhost:8010 (в контейнере)
```

Откройте `frontend/index.html` в браузере и загрузите PDF. Фронт обратится к `http://localhost:8080/process`.

## Структура

- `docker-compose.yml` — поднимает API и LanguageTool
- `backend/` — FastAPI + OCR + Grammar + Export
- `frontend/` — простой HTML‑клиент
- `data/` — результаты (страницы, JSON, DOCX) — создаётся при запуске

## Примечания
- В backend‑контейнере установлены: `tesseract-ocr`, `tesseract-ocr-deu`, `poppler-utils` — интернет не нужен.
- Для рукописного OCR можно добавить движок TrOCR/ONNX (отдельный сервис) и переключение `/process?engine=handwritten`.
- Экспорт DOCX упрощённо вставляет HTML‑подсветку как текст; для глянцевой разметки используйте HTML/PDF экспорт (например, WeasyPrint).

## Лицензия
MIT
