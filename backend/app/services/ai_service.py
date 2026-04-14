import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_cv_job(cv_text: str, job_text: str) -> dict:
    prompt = f"""
You are a senior technical recruiter and career coach.

Analyze the following CV and job description.

Return ONLY a valid JSON. No explanations. No extra text.

If you fail to return valid JSON, your response is useless.

Structure:
{{
  "match_score": number,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "cv_improvements": [],
  "project_suggestions": []
}}

CV:
{cv_text}

JOB DESCRIPTION:
{job_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You ONLY return valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "error": "Invalid JSON from model",
            "raw_output": content
        }