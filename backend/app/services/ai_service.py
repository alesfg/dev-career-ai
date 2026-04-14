from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_cv_job(cv_text: str, job_text: str) -> dict:
    prompt = f"""
You are a senior technical recruiter and career coach.

Analyze the following CV and job description.

CV:
{cv_text}

JOB DESCRIPTION:
{job_text}

Return ONLY a JSON with:
- match_score (0-100)
- strengths (list)
- weaknesses (list)
- missing_skills (list)
- cv_improvements (list)
- project_suggestions (list)

Be specific and practical.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert recruiter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    return content