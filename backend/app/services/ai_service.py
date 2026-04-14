import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def extract_cv(cv_text: str) -> dict:
    prompt = f"""
Extract structured information from this CV.

Return ONLY JSON with:
- skills
- experience
- technologies
- seniority (junior, mid, senior)

CV:
{cv_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return safe_json(response.choices[0].message.content)


def extract_job(job_text: str) -> dict:
    prompt = f"""
Extract structured information from this job description.

Return ONLY JSON with:
- required_skills
- technologies
- seniority
- responsibilities

JOB:
{job_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return safe_json(response.choices[0].message.content)


def compare_and_generate(cv_data: dict, job_data: dict) -> dict:
    prompt = f"""
You are a senior recruiter.

Compare this candidate with the job.

CV DATA:
{cv_data}

JOB DATA:
{job_data}

Return ONLY JSON:
{{
  "match_score": number,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "cv_improvements": [],
  "project_suggestions": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return safe_json(response.choices[0].message.content)


def safe_json(content: str) -> dict:
    try:
        return json.loads(content)
    except:
        return {
            "error": "Invalid JSON",
            "raw_output": content
        }