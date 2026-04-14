from fastapi import APIRouter, UploadFile, File, Form
from app.services.analysis_service import run_analysis
from app.services.pdf_service import extract_text_from_pdf, clean_text

router = APIRouter()

@router.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    job_text: str = Form(...)
):
    raw_text = extract_text_from_pdf(file.file)
    cv_text = clean_text(raw_text)

    result = run_analysis(cv_text, job_text)

    return result