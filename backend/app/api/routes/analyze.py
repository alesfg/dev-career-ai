from fastapi import APIRouter
from app.schemas.analysis import AnalyzeRequest
from app.services.analysis_service import run_analysis

router = APIRouter()

@router.post("/analyze")
def analyze(data: AnalyzeRequest):
    return run_analysis(data.cv_text, data.job_text)