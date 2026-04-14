from fastapi import APIRouter
from app.schemas.analysis import AnalyzeRequest

router = APIRouter()

@router.post("/analyze")
def analyze(data: AnalyzeRequest):
    return {
        "message": "Endpoint working",
        "cv_length": len(data.cv_text),
        "job_length": len(data.job_text)
    }