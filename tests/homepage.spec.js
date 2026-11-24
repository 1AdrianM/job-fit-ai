// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Job Fit AI - Homepage', () => {
  test('should load homepage successfully', async ({ page }) => {
    await page.goto('/');
    
    // Check title (new Vercel+Notion design)
    await expect(page).toHaveTitle(/Job Fit AI/);
    
    // Check main heading (now "Professional Job Analysis")
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
    await expect(h1).toContainText('Professional Job Analysis');
  });

  test('should have analysis form with required fields', async ({ page }) => {
    await page.goto('/');
    
    // Check CV textarea
    const cvField = page.locator('textarea[name="cv"]');
    await expect(cvField).toBeVisible();
    
    // Check job description textarea
    const jobField = page.locator('textarea[name="job_description"]');
    await expect(jobField).toBeVisible();
    
    // Check submit button
    const submitBtn = page.locator('button[type="submit"]');
    await expect(submitBtn).toBeVisible();
  });

  test('should display feature cards', async ({ page }) => {
    await page.goto('/');
    
    // Check that feature section exists
    const features = page.locator('text=/Fit Score|Cover Letter|Gap/i');
    const count = await features.count();
    expect(count).toBeGreaterThan(0);
  });
});
