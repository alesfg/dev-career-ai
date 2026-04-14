from fastapi import APIRouter
from app.schemas.analysis import AnalyzeRequest
from app.services.ai_service import analyze_cv_job

router = APIRouter()

@router.post("/analyze")
def analyze(data: AnalyzeRequest):
    result = analyze_cv_job(data.cv_text, data.job_text)

    return {
        "analysis": result
    }