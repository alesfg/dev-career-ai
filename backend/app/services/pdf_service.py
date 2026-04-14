import pdfplumber
import re

def extract_text_from_pdf(file) -> str:
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)  # múltiples espacios → 1
    return text.strip()