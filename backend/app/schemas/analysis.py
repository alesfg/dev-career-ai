from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    cv_text: str
    job_text: str