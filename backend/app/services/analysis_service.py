from app.services.ai_service import (
    extract_cv,
    extract_job,
    compare_and_generate,
    rewrite_cv
)


def run_analysis(cv_text: str, job_text: str) -> dict:
    cv_data = extract_cv(cv_text)
    job_data = extract_job(job_text)

    analysis = compare_and_generate(cv_data, job_data)

    rewritten = rewrite_cv(cv_text, job_text, analysis)

    return {
        "cv_data": cv_data,
        "job_data": job_data,
        "analysis": analysis,
        "rewritten_cv": rewritten
    }