// @ts-check

/**
 * Common test utilities and helpers for Playwright tests
 */

/**
 * Sample CV data for testing
 */
const sampleData = {
  cv: {
    full: `Adrian Mateo
Backend Developer
Email: adrianbatista025@gmail.com
LinkedIn: linkedin.com/in/adrian-mateo-425a03257

SKILLS:
Java, Spring Boot, Python, FastAPI, Node.js, PostgreSQL, Docker, AWS, Hexagonal Architecture

EXPERIENCE:
Backend Developer | 2 years
- Built RESTful APIs with Java Spring Boot serving 10k+ daily requests
- Implemented fraud detection system (SentinelPay) with 95% accuracy
- Developed AI-powered solutions with FastAPI and Google Gemini
- Deployed microservices to AWS using Docker and Kubernetes

PROJECTS:
- SentinelPay: Real-time fraud detection using Java/Spring Boot/Hexagonal Architecture
- Chief Wiggum: AI agent supervisor system with TypeScript/Node.js
- Job Fit AI: FastAPI + Google Gemini for intelligent job matching
- Talon: Price intelligence platform for Shopify/Amazon resellers`,

    minimal: 'Adrian Mateo\nBackend Developer with 2 years of Java/Spring Boot experience',
    
    invalid: 'x',
  },
  
  job: {
    full: `Junior Backend Developer
Company: TechCorp Inc.
Location: Remote (LATAM)

ABOUT THE ROLE:
We're looking for a passionate Junior Backend Developer to join our growing team.

REQUIREMENTS:
- 2+ years experience with Java/Spring Boot
- Strong understanding of RESTful API design
- Experience with SQL databases (PostgreSQL/MySQL)
- Knowledge of Docker and containerization
- Git version control proficiency
- Excellent problem-solving skills
- English proficiency (C1)

NICE TO HAVE:
- AWS or cloud platform experience
- Python/FastAPI knowledge
- Microservices architecture exposure
- AI/ML interest
- Open source contributions

BENEFITS:
- Competitive salary in USD
- 100% remote work
- Flexible hours
- Learning budget`,

    minimal: 'Java Backend Developer position requiring 2 years experience',
    
    invalid: 'y',
  }
};

/**
 * Common page actions
 */
const actions = {
  /**
   * Fill the CV and job description form
   */
  async fillAnalysisForm(page, cvText, jobText) {
    await page.locator('textarea[name="cv"]').first().fill(cvText);
    await page.locator('textarea[name="job_description"]').first().fill(jobText);
  },
  
  /**
   * Submit the analysis form
   */
  async submitForm(page) {
    const submitButton = page.locator('button[type="submit"]').first();
    await submitButton.click();
  },
  
  /**
   * Wait for analysis results
   */
  async waitForResults(page, timeout = 30000) {
    return await page.waitForSelector(
      '.results, #results, [data-testid="results"]',
      { timeout }
    );
  },
};

/**
 * Common assertions
 */
const assertions = {
  /**
   * Check if page has expected structure
   */
  async hasBasicStructure(page, expect) {
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('textarea[name="cv"]').first()).toBeVisible();
    await expect(page.locator('textarea[name="job_description"]').first()).toBeVisible();
  },
};

/**
 * Screenshot helpers
 */
const screenshots = {
  async capture(page, name, options = {}) {
    const path = `tests/screenshots/${name}.png`;
    await page.screenshot({ 
      path, 
      fullPage: options.fullPage !== false,
      ...options 
    });
    return path;
  },
  
  async captureElement(page, selector, name) {
    const element = await page.locator(selector).first();
    await element.screenshot({ path: `tests/screenshots/${name}.png` });
  },
};

module.exports = {
  sampleData,
  actions,
  assertions,
  screenshots,
};
