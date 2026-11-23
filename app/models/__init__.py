from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CVData(BaseModel):
    """User's CV data."""
    full_text: str
    skills: list[str] = []
    experience_years: float
    education: str
    projects: list[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class JobDescription(BaseModel):
    """Job posting data."""
    title: str
    company: Optional[str] = None
    description: str
    requirements: list[str] = []
    nice_to_have: list[str] = []
    url: Optional[str] = None


class FitAnalysis(BaseModel):
    """AI analysis result."""
    fit_score: float = Field(..., ge=0, le=100)
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    concerns: list[str]
    reasoning: str


class CoverLetter(BaseModel):
    """Generated cover letter."""
    content: str
    tone: str = "professional"
    word_count: int


class JobAnalysisRequest(BaseModel):
    """Request to analyze a job."""
    job_description: str
    cv: Optional[str] = None  # Optional CV text from form
    cv_id: Optional[int] = None  # Optional CV ID from database


class JobAnalysisResponse(BaseModel):
    """Complete analysis response."""
    job: JobDescription
    analysis: FitAnalysis
    cover_letter: CoverLetter
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
