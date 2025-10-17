FROM python:3.11-slim

# System deps: tesseract (with German), poppler (pdf2image), fonts
RUN apt-get update && apt-get install -y --no-install-recommends     tesseract-ocr tesseract-ocr-deu poppler-utils     locales fonts-dejavu-core &&     rm -rf /var/lib/apt/lists/*

# Locale
RUN sed -i 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN mkdir -p /app/data

EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
