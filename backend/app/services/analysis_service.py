from app.agents.career_agent import build_agent


agent = build_agent()


def run_analysis(cv_text: str, job_text: str) -> dict:
    result = agent.invoke({
        "cv_text": cv_text,
        "job_text": job_text
    })

    return result