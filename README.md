# 🎯 Job Fit AI - Intelligent Job Application Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

**AI-powered tool to analyze job fit, generate tailored cover letters, and accelerate your job search.**

Built to solve a real problem: applying to dozens of jobs efficiently while maintaining quality and personalization.

---

## 🚀 Why This Exists

Job searching is time-consuming. For every opening, you need to:
- ✅ Analyze if you're a good fit
- ✅ Identify gaps in your experience
- ✅ Write a personalized cover letter
- ✅ Track keywords to emphasize

**Job Fit AI automates this in seconds.**

---

## ✨ Features

### MVP (Phase 1)
- 📄 **Job Description Analysis**: Paste or upload JD → get structured breakdown
- 🎯 **Fit Score**: AI-powered match percentage vs your CV
- ✍️ **Cover Letter Generator**: Personalized, professional cover letters in seconds
- 🔍 **Gap Analysis**: Missing skills/keywords highlighted
- 💾 **Job Tracker**: Save analyzed jobs with notes

### Coming Soon (Phase 2)
- 🌐 **URL Scraper**: Analyze job postings from LinkedIn/Indeed/etc directly
- 📊 **Dashboard**: Track applications, fit scores, and follow-ups
- 🤖 **Multi-CV Support**: Different CVs for different job types
- 📧 **Email Templates**: Auto-generate follow-up emails

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **LLM**: Google Gemini 1.5 Pro (best for text analysis, free tier)
- **Frontend**: HTMX + TailwindCSS (simple, reactive)
- **Database**: SQLite (MVP) → PostgreSQL (production)
- **Deployment**: Railway (free tier)

---

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API key ([get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone repo
git clone https://github.com/1AdrianM/job-fit-ai.git
cd job-fit-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run app
uvicorn app.main:app --reload
```

Open http://localhost:8000

---

## 📸 Screenshots

_Coming soon after MVP deployment_

---

## 🎯 How It Works

1. **Upload your CV** (one-time setup)
2. **Paste job description** from any source
3. **Get instant analysis**:
   - Fit score (0-100%)
   - Matching skills highlighted
   - Missing requirements flagged
   - Generated cover letter
4. **Save or export** results

---

## 🧪 Architecture

```
job-fit-ai/
├── app/
│   ├── api/          # FastAPI routes
│   ├── core/         # Config, security
│   ├── models/       # Pydantic models
│   ├── services/     # Business logic (AI, parsing)
│   ├── static/       # CSS, JS
│   └── templates/    # HTML (Jinja2)
├── tests/
├── requirements.txt
└── README.md
```

**Key Design Decisions**:
- **FastAPI** over Flask: Better async support, automatic OpenAPI docs
- **Gemini 1.5 Pro** over GPT-4/Claude: Free tier, excellent text analysis, fast
- **HTMX** over React: Simpler, faster to build, no build step
- **SQLite MVP**: Deploy immediately, migrate to Postgres later

---

## 🚧 Roadmap

- [x] Project setup
- [ ] CV parser
- [ ] Job description analyzer
- [ ] Fit score algorithm
- [ ] Cover letter generator
- [ ] Basic UI (HTMX)
- [ ] Deploy to Railway
- [ ] URL scraper (LinkedIn/Indeed)
- [ ] Application tracker dashboard

---

## 📝 License

MIT License - feel free to use this for your own job search!

---

## 🤝 Contributing

Built as a portfolio project, but PRs welcome! Open an issue first to discuss changes.

---

## 🧪 Testing

Automated E2E tests with Playwright:

```bash
# Run all tests
npm test

# Run tests in UI mode (recommended)
npm run test:ui

# View test report
npm run test:report
```

**Test Coverage:**
- Homepage rendering and navigation
- Form validation and submission
- API integration tests
- Responsive design (mobile, tablet, desktop)
- Accessibility checks
- Performance monitoring

See [tests/README.md](tests/README.md) for detailed documentation.

---

## 📫 Contact

**Adrián Mateo**  
Backend Engineer | AI Enthusiast  
[LinkedIn](https://www.linkedin.com/in/adrian-mateo-425a03257/) | [GitHub](https://github.com/1AdrianM) | [Email](mailto:adrianbatista025@gmail.com)

---

<div align="center">
  
*"Built this to land my next role. Hope it helps you land yours."*

</div>
