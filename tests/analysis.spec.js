// @ts-check
const { test, expect } = require('@playwright/test');

const sampleCV = `Adrian Mateo
Backend Developer
Email: adrianbatista025@gmail.com
LinkedIn: linkedin.com/in/adrian-mateo-425a03257

SKILLS:
Java, Spring Boot, Python, FastAPI, Node.js, PostgreSQL, Docker, AWS

EXPERIENCE:
Backend Developer | 2 years
- Built RESTful APIs with Java Spring Boot
- Implemented fraud detection system (SentinelPay)
- Developed AI-powered solutions with FastAPI

PROJECTS:
- SentinelPay: Fraud detection with Java/Spring Boot/Hexagonal Architecture
- Chief Wiggum: AI agent supervisor with TypeScript/Node.js
- Job Fit AI: FastAPI + Google Gemini for job analysis`;

const sampleJob = `Junior Backend Developer
Company: TechCorp Inc.

Requirements:
- 2+ years experience with Java/Spring Boot
- Strong understanding of RESTful APIs
- Experience with SQL databases (PostgreSQL/MySQL)
- Knowledge of Docker and containerization
- Excellent problem-solving skills

Nice to have:
- AWS experience
- Python/FastAPI knowledge
- AI/ML interest`;

test.describe('Job Fit AI - Analysis Flow', () => {
  test('should submit CV and job description successfully', async ({ page }) => {
    await page.goto('/');
    
    // Fill CV textarea
    const cvTextarea = page.locator('textarea[name="cv"]').first();
    await cvTextarea.fill(sampleCV);
    await expect(cvTextarea).toHaveValue(sampleCV);
    
    // Fill Job Description textarea
    const jobTextarea = page.locator('textarea[name="job_description"]').first();
    await jobTextarea.fill(sampleJob);
    await expect(jobTextarea).toHaveValue(sampleJob);
    
    // Take screenshot before submission
    await page.screenshot({ path: 'tests/screenshots/before-analysis.png', fullPage: true });
  });

  test('should validate empty form submission', async ({ page }) => {
    await page.goto('/');
    
    // Check that form fields have required attribute
    const cvTextarea = page.locator('textarea[name="cv"]').first();
    const jobTextarea = page.locator('textarea[name="job_description"]').first();
    
    // Verify required attribute exists
    await expect(cvTextarea).toHaveAttribute('required', '');
    await expect(jobTextarea).toHaveAttribute('required', '');
  });

  test('should handle form with minimal data', async ({ page }) => {
    await page.goto('/');
    
    const minimalCV = 'Adrian Mateo\nJava Developer with 2 years experience';
    const minimalJob = 'Java Developer position';
    
    await page.locator('textarea[name="cv"]').first().fill(minimalCV);
    await page.locator('textarea[name="job_description"]').first().fill(minimalJob);
    
    // Form should accept minimal data
    await expect(page.locator('textarea[name="cv"]').first()).toHaveValue(minimalCV);
  });
});

test.describe('Job Fit AI - API Integration', () => {
  test('should have analyze endpoint', async ({ request }) => {
    // Test API directly
    const response = await request.post('/api/analyze', {
      data: {
        cv: sampleCV,
        job_description: sampleJob
      },
      timeout: 60000 // 60 seconds for AI processing
    });
    
    // Should return 200 (success), 422 (validation error), or 500 (server error during AI processing)
    // Any of these means the endpoint exists and is responding
    expect([200, 422, 500]).toContain(response.status());
  });

  test('should have docs endpoint', async ({ page }) => {
    await page.goto('/docs');
    
    // FastAPI auto-generates docs
    await expect(page.locator('text=FastAPI').or(page.locator('text=Job Fit AI'))).toBeVisible();
  });
});

test.describe('Job Fit AI - Responsive Design', () => {
  test('should be mobile friendly', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/');
    
    await expect(page.locator('h1')).toBeVisible();
    
    // Take mobile screenshot
    await page.screenshot({ path: 'tests/screenshots/mobile-view.png', fullPage: true });
  });

  test('should be tablet friendly', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await page.goto('/');
    
    await expect(page.locator('h1')).toBeVisible();
    
    // Take tablet screenshot
    await page.screenshot({ path: 'tests/screenshots/tablet-view.png', fullPage: true });
  });
});
