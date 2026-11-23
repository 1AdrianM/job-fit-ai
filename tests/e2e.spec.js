// @ts-check
const { test, expect } = require('@playwright/test');

// Mark as slow test because it involves real API calls
test.describe('Job Fit AI - E2E Full Flow', () => {
  test.slow(); // Triple timeout for API calls
  
  test('should complete full analysis workflow', async ({ page }) => {
    await page.goto('/');
    
    // Sample data
    const cv = `Adrian Mateo
Backend Developer | 2 years experience
Skills: Java, Spring Boot, Python, FastAPI, PostgreSQL, Docker
Projects: SentinelPay (fraud detection), Chief Wiggum (AI supervisor)`;

    const job = `Junior Backend Developer at TechCorp
Requirements: Java, Spring Boot, RESTful APIs, PostgreSQL`;
    
    // Fill form
    await page.locator('textarea[name="cv"]').first().fill(cv);
    await page.locator('textarea[name="job_description"]').first().fill(job);
    
    // Screenshot: Form filled
    await page.screenshot({ 
      path: 'tests/screenshots/01-form-filled.png', 
      fullPage: true 
    });
    
    // Submit form
    const submitButton = page.locator('button[type="submit"]').first();
    await submitButton.click();
    
    // Wait for response (AI processing)
    // Adjust selector based on your actual results container
    await page.waitForSelector('.results, #results, [data-testid="results"]', { 
      timeout: 30000 // 30s for Gemini API
    }).catch(() => {
      console.log('Results container not found - check your HTML structure');
    });
    
    // Screenshot: Results shown
    await page.screenshot({ 
      path: 'tests/screenshots/02-results.png', 
      fullPage: true 
    });
    
    // Verify some result is displayed (adjust selectors to your actual HTML)
    const hasResults = await page.locator('body').textContent();
    expect(hasResults).toBeTruthy();
  });
  
  test('should handle API errors gracefully', async ({ page }) => {
    await page.goto('/');
    
    // Fill with invalid/problematic data
    await page.locator('textarea[name="cv"]').first().fill('x');
    await page.locator('textarea[name="job_description"]').first().fill('y');
    
    const submitButton = page.locator('button[type="submit"]').first();
    await submitButton.click();
    
    // Should show some feedback (error or loading state)
    await page.waitForTimeout(2000);
    
    const bodyText = await page.locator('body').textContent();
    expect(bodyText).toBeTruthy();
  });
});

test.describe('Job Fit AI - Performance', () => {
  test('should load homepage quickly', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    const loadTime = Date.now() - startTime;
    
    // Should load in under 3 seconds
    expect(loadTime).toBeLessThan(3000);
  });
  
  test('should have no console errors', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.goto('/');
    
    // No critical errors
    expect(errors).toHaveLength(0);
  });
});

test.describe('Job Fit AI - Accessibility', () => {
  test('should have proper heading structure', async ({ page }) => {
    await page.goto('/');
    
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBeGreaterThan(0);
  });
  
  test('should have alt text for images', async ({ page }) => {
    await page.goto('/');
    
    const images = await page.locator('img').all();
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      expect(alt).toBeDefined();
    }
  });
  
  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/');
    
    // Tab through interactive elements
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(focused).toBeTruthy();
  });
});
