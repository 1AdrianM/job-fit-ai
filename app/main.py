"""
Job Fit AI - FastAPI Application
"""

import httpx
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.models import CVData, JobAnalysisRequest, JobAnalysisResponse, JobDescription
from app.services.ai_service import AIService
from app.services.cv_parser_service import CVParserService
from app.services.history_service import HistoryService
from app.services.scraper_service import JobScraperService

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
scraper_service = JobScraperService()
cv_parser_service = CVParserService()
history_service = HistoryService()


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

    # Save to history
    history_service.save_analysis(
        cv_text=job_data.cv,
        job_description=job_data.job_description,
        analysis=analysis,
        cover_letter=cover_letter,
    )

    # Check if request is from HTMX
    if request.headers.get("HX-Request"):
        # Return HTML for HTMX
        return templates.TemplateResponse(
            "results.html",
            {"request": request, "analysis": analysis, "cover_letter": cover_letter, "job": job},
        )

    # Return JSON for direct API calls
    return JobAnalysisResponse(job=job, analysis=analysis, cover_letter=cover_letter)


@app.post("/api/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload and parse CV file (PDF or DOCX).

    Accepts a CV file upload and returns the extracted text.
    """
    # Validate file
    is_valid, error_message = cv_parser_service.validate_file(
        file.content_type or "", file.size or 0
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    # Read file content
    try:
        file_content = await file.read()

        # Parse CV
        cv_text = cv_parser_service.parse_cv(file_content, file.filename or "")

        if not cv_text or len(cv_text.strip()) < 50:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract enough text from CV. "
                    "Please ensure the file is not password-protected or corrupted."
                ),
            )

        return JSONResponse({"success": True, "cv_text": cv_text, "filename": file.filename})

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")


@app.post("/api/scrape-job")
async def scrape_job(request: Request):
    """
    Scrape job description from a URL.

    Accepts a job posting URL and returns the extracted job description.
    """
    data = await request.json()
    job_url = data.get("url", "").strip()

    if not job_url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Validate URL
    if not scraper_service.validate_url(job_url):
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid or unsupported job posting URL. "
                "Supported platforms: LinkedIn, Indeed, Greenhouse, Lever, and others."
            ),
        )

    try:
        # Fetch the page
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(
                job_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )
            response.raise_for_status()

        # Extract job description
        job_description = scraper_service.extract_job_description(response.text, job_url)

        if not job_description:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract job description from this URL. "
                    "Please try copying the text manually."
                ),
            )

        return JSONResponse({"success": True, "job_description": job_description, "url": job_url})

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch job posting: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping job: {str(e)}")


@app.get("/api/history")
async def get_history(limit: int = 20):
    """
    Get list of recent job analyses.

    Returns a list of analysis summaries sorted by most recent first.
    """
    try:
        history = history_service.get_history(limit=limit)
        return JSONResponse({"success": True, "history": history})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@app.get("/api/history/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get a specific analysis by ID.

    Returns the full analysis data including CV, job description,
    analysis results, and cover letter.
    """
    analysis = history_service.get_analysis(analysis_id)

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return JSONResponse({"success": True, "analysis": analysis})


@app.delete("/api/history/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    Delete a specific analysis from history.
    """
    deleted = history_service.delete_analysis(analysis_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return JSONResponse({"success": True, "message": "Analysis deleted"})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
