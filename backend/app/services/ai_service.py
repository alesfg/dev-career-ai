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
        # limpiar markdown ```json ```
        content = content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except Exception as e:
        return {
            "error": "Invalid JSON",
            "raw_output": content,
            "details": str(e)
        }
    
def rewrite_cv(cv_text: str, job_text: str, analysis: dict) -> dict:
    prompt = f"""
You are an expert technical recruiter.

Rewrite the CV to better match the job description.

Rules:
- Keep it realistic (do not invent fake experience)
- Emphasize relevant skills
- Use strong action verbs
- Optimize for ATS keywords
- Make it concise and impactful

Format the CV in a clean, professional structure with sections:
- Summary
- Experience
- Skills
- Projects

ORIGINAL CV:
{cv_text}

JOB DESCRIPTION:
{job_text}

ANALYSIS:
{analysis}

Return ONLY JSON:
{{
  "rewritten_cv": "full rewritten CV text",
  "key_changes": ["list of main improvements made"]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return safe_json(response.choices[0].message.content)

def generate_roadmap(analysis: dict) -> dict:
    prompt = f"""
You are an expert career coach for software engineers.

Based on this analysis:
{analysis}

Create a practical improvement roadmap.

Rules:
- Be realistic
- Focus on high-impact skills
- Include specific actions
- Keep it concise

Return ONLY JSON:
{{
  "roadmap": [
    {{
      "week": 1,
      "focus": "skill or topic",
      "actions": ["specific tasks"]
    }}
  ],
  "priority_skills": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return safe_json(response.choices[0].message.content)