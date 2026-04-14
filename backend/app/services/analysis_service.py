from app.services.ai_service import extract_cv, extract_job, compare_and_generate


def run_analysis(cv_text: str, job_text: str) -> dict:
    cv_data = extract_cv(cv_text)
    job_data = extract_job(job_text)

    result = compare_and_generate(cv_data, job_data)

    return {
        "cv_data": cv_data,
        "job_data": job_data,
        "analysis": result
    }