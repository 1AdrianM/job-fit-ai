"""
Job Fit AI - FastAPI Application
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.models import CVData, JobAnalysisRequest, JobAnalysisResponse, JobDescription
from app.services.ai_service import AIService

# Initialize app
settings = get_settings()
app = FastAPI(
    title=settings.app_name, description="AI-powered job application assistant", version="0.1.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize AI service
ai_service = AIService()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with job analysis form."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/analyze")
async def analyze_job(request: Request, job_data: JobAnalysisRequest):
    """
    Analyze a job description against the user's CV.

    Returns fit score, analysis, and generated cover letter.
    Can return JSON or HTML depending on request (HTMX vs direct API call).
    """
    # Use provided CV or fallback to default
    if job_data.cv:
        # Parse CV from form input
        cv = CVData(
            full_text=job_data.cv,
            skills=[],  # TODO: Extract skills with AI
            experience_years=2.0,  # TODO: Extract from CV
            education="",  # TODO: Extract from CV
            projects=[],
        )
    else:
        # Use default CV (for testing/demo)
        cv = CVData(
            full_text="""
        Adrián Julio Mateo Batista
        Backend Engineer | Dominican Republic

        EXPERIENCE:
        - 1.5-2 years backend development
        - Built fraud detection system with Java/Spring Boot
        - Developed distributed key-value store
        - Created e-commerce backend with microservices
        - ~1 year AI/LLM integration experience

        SKILLS:
        - Java (Spring Boot, Spring Security, Spring AI)
        - Python (FastAPI, LLM APIs, embeddings, agents)
        - TypeScript/JavaScript, Go
        - PostgreSQL, MySQL, SQL Server, Qdrant
        - Docker, Kubernetes, OpenShift
        - REST APIs, gRPC, microservices
        - Clean/Hexagonal Architecture, DDD

        PROJECTS:
        - SentinelPay: Real-time fraud detection (Java/Spring Boot/Hexagonal Architecture)
        - Chief Wiggum: AI agent supervisor (TypeScript/Node.js)
        - Talon: Price intelligence platform for Shopify/Amazon resellers
        - E-commerce backend with AI recommendations
        """,
            skills=[
                "Java",
                "Spring Boot",
                "Python",
                "FastAPI",
                "TypeScript",
                "PostgreSQL",
                "Docker",
                "Kubernetes",
                "REST APIs",
                "Microservices",
                "AI",
                "LLM",
                "RAG",
                "Vector Search",
                "Clean Architecture",
            ],
            experience_years=1.75,
            education="Computer Science / Software Engineering",
            projects=["SentinelPay", "Chief Wiggum", "Talon", "E-commerce + AI"],
        )

    # Parse job description
    job = JobDescription(
        title="Extracted from description",
        description=job_data.job_description,
        requirements=[],  # TODO: Extract with AI
    )

    # Analyze fit
    analysis = await ai_service.analyze_job_fit(cv, job)

    # Generate cover letter
    cover_letter = await ai_service.generate_cover_letter(cv, job, analysis)

    # Check if request is from HTMX
    if request.headers.get("HX-Request"):
        # Return HTML for HTMX
        return templates.TemplateResponse(
            "results.html",
            {"request": request, "analysis": analysis, "cover_letter": cover_letter, "job": job},
        )

    # Return JSON for direct API calls
    return JobAnalysisResponse(job=job, analysis=analysis, cover_letter=cover_letter)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
