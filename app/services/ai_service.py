"""
AI Service for job analysis using Google Gemini.
"""

import json

import google.generativeai as genai

from app.config import get_settings
from app.models import CoverLetter, CVData, FitAnalysis, JobDescription


class AIService:
    """Service for AI-powered job analysis using Gemini."""

    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analyze_job_fit(self, cv: CVData, job: JobDescription) -> FitAnalysis:
        """
        Analyze how well a CV matches a job description.

        Returns fit score, matching/missing skills, and reasoning.
        """
        prompt = self._build_analysis_prompt(cv, job)

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
        )

        # Parse JSON response from Gemini
        result_text = response.text
        # Clean markdown code blocks if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        result = json.loads(result_text)

        return FitAnalysis(**result)

    async def generate_cover_letter(
        self, cv: CVData, job: JobDescription, analysis: FitAnalysis
    ) -> CoverLetter:
        """Generate a personalized cover letter."""
        prompt = self._build_cover_letter_prompt(cv, job, analysis)

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1500,
            },
        )

        content = response.text
        word_count = len(content.split())

        return CoverLetter(content=content, tone="professional", word_count=word_count)

    def _build_analysis_prompt(self, cv: CVData, job: JobDescription) -> str:
        """Build prompt for job fit analysis."""
        return f"""You are an expert career advisor analyzing job fit.

**Candidate CV:**
{cv.full_text}

Skills: {", ".join(cv.skills)}
Experience: {cv.experience_years} years
Education: {cv.education}

**Job Description:**
Title: {job.title}
Company: {job.company or "Not specified"}
{job.description}

Requirements: {", ".join(job.requirements) if job.requirements else "See description"}

**Task:**
Analyze how well this candidate matches this job. Return ONLY valid JSON with this structure:

{{
  "fit_score": <number 0-100>,
  "matching_skills": [<list of skills from CV that match job requirements>],
  "missing_skills": [<list of required skills candidate lacks>],
  "strengths": [<3-4 bullet points of why candidate is strong>],
  "concerns": [<2-3 bullet points of potential gaps or risks>],
  "reasoning": "<2-3 sentence summary of overall fit>"
}}

Be honest but constructive. Focus on transferable skills.
Return ONLY the JSON, no extra text before or after."""

    def _build_cover_letter_prompt(
        self, cv: CVData, job: JobDescription, analysis: FitAnalysis
    ) -> str:
        """Build prompt for cover letter generation."""
        return f"""You are an expert cover letter writer.

**Candidate CV:**
{cv.full_text}

**Job:**
{job.title} at {job.company or "the company"}

**Fit Analysis:**
- Fit Score: {analysis.fit_score}%
- Matching Skills: {", ".join(analysis.matching_skills)}
- Strengths: {", ".join(analysis.strengths)}

**Task:**
Write a professional cover letter (250-350 words) that:
1. Opens with genuine interest in the role
2. Highlights the candidate's most relevant experience
3. Addresses 2-3 key matching skills from the analysis
4. Shows enthusiasm without being generic
5. Closes with a clear call to action

Tone: Professional but personable. No clichés or buzzwords.
Do NOT include address/date header or "Sincerely" closing - just the body.

Write the cover letter now:"""
