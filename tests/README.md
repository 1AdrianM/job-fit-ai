# 🎭 Playwright E2E Testing

Automated end-to-end tests for Job Fit AI using Playwright.

## 📋 Test Coverage

### ✅ Homepage Tests (`homepage.spec.js`)
- Homepage loads successfully
- Navigation works correctly
- Feature cards are visible

### ✅ Analysis Flow Tests (`analysis.spec.js`)
- Form submission with CV and job description
- Form validation for empty submissions
- Minimal data handling
- API endpoint tests
- Responsive design (mobile, tablet, desktop)

### ✅ E2E Full Flow (`e2e.spec.js`)
- Complete analysis workflow with real API calls
- Error handling
- Performance checks
- Accessibility tests

## 🚀 Running Tests

### Prerequisites
```bash
# Install dependencies (first time only)
npm install
```

### Run all tests
```bash
npm test
```

### Run tests in UI mode (recommended for development)
```bash
npm run test:ui
```

### Run tests with browser visible
```bash
npm run test:headed
```

### Debug mode (step through tests)
```bash
npm run test:debug
```

### View test report
```bash
npm run test:report
```

### Generate new tests (record your actions)
```bash
npm run test:codegen
```

## 📸 Screenshots

Tests automatically capture screenshots:
- **On failure**: Screenshots and videos saved to `test-results/`
- **Manual screenshots**: Saved to `tests/screenshots/`

Generated screenshots:
- `before-analysis.png` - Form filled, before submission
- `01-form-filled.png` - E2E test form state
- `02-results.png` - E2E test results
- `mobile-view.png` - Mobile responsive test
- `tablet-view.png` - Tablet responsive test

## 📁 Structure

```
tests/
├── homepage.spec.js      # Homepage tests
├── analysis.spec.js      # Analysis flow tests
├── e2e.spec.js          # Full E2E workflow tests
└── screenshots/         # Manual screenshots

playwright.config.js      # Playwright configuration
playwright-report/       # HTML test reports (after running tests)
test-results/           # Test artifacts (screenshots, videos on failure)
```

## 🔧 Configuration

Edit `playwright.config.js` to:
- Change timeouts
- Add more browsers (Firefox, Safari)
- Modify screenshot/video settings
- Change parallelization

## 🧪 Writing New Tests

Create a new spec file:

```javascript
// tests/my-feature.spec.js
const { test, expect } = require('@playwright/test');

test('my new test', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toBeVisible();
});
```

## 📊 CI/CD Integration

Tests automatically run with:
- 2 retries on failure (CI only)
- Video recording on failure
- HTML report generation

Add to GitHub Actions:
```yaml
- name: Install dependencies
  run: |
    npm ci
    npx playwright install --with-deps chromium

- name: Run Playwright tests
  run: npm test
  
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

## 🐛 Troubleshooting

### Server not starting
Make sure the FastAPI server is accessible:
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

### Browser download issues
Install browsers manually:
```bash
npx playwright install chromium
```

### Tests timing out
Increase timeout in `playwright.config.js`:
```javascript
timeout: 60 * 1000, // 60 seconds
```

## 📚 Resources

- [Playwright Documentation](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-test)
