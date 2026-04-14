from fastapi import FastAPI
from app.api.routes.analyze import router as analyze_router

app = FastAPI(
    title="Dev Career AI Agent",
    description="AI system to analyze CVs vs job offers",
    version="0.1.0"
)

app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Dev Career AI Agent API is running"}