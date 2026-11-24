# 🔄 Development Loop - Feature Development Workflow

## 🎯 Overview

This is your complete development cycle from feature idea to production.

```
Feature Idea → Local Dev → Tests → PR → CI/CD → Merge → Production
     ↓                                                        ↓
   Done! ←─────────────────── Auto-Deploy ←─────────────────┘
```

---

## 📋 Complete Workflow

### **STEP 1: Start New Feature** (2 min)

```bash
# Option A: Use helper script (recommended)
./scripts/gitflow.sh feature start my-feature-name

# Option B: Manual
git checkout develop
git pull origin develop
git checkout -b feature/my-feature-name
```

**Example feature names:**
- `feature/cv-upload`
- `feature/job-scraper`
- `feature/email-results`
- `feature/pdf-export`

---

### **STEP 2: Develop Locally** (variable time)

**Start local server:**
```bash
# Activate venv
source venv/bin/activate

# Start FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Open in browser:**
```
http://localhost:8000
```

**Make your changes:**
- Edit files in `app/`
- Server auto-reloads on save
- Test manually in browser

---

### **STEP 3: Write/Update Tests** (10-20 min)

**Add Playwright test:**
```javascript
// tests/my-feature.spec.js
const { test, expect } = require('@playwright/test');

test('my new feature works', async ({ page }) => {
  await page.goto('/');
  
  // Your test here
  await page.click('#my-button');
  await expect(page.locator('#result')).toBeVisible();
});
```

**Run tests locally:**
```bash
# Run all tests
npm test

# Run specific test
npx playwright test tests/my-feature.spec.js

# Run with UI
npx playwright test --ui

# Debug mode
npx playwright test --debug
```

**Tests must pass locally before PR!**

---

### **STEP 4: Code Quality Check** (2 min)

```bash
# Linting
ruff check app/

# Auto-fix issues
ruff check app/ --fix

# Format code
ruff format app/

# Verify all clean
ruff check app/ && ruff format app/ --check
```

**All checks must pass!**

---

### **STEP 5: Commit Changes** (1 min)

**Follow Conventional Commits:**

```bash
git add .

# Format: <type>: <description>
git commit -m "feat: add CV upload functionality"
```

**Commit types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Add/update tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

**Examples:**
```bash
git commit -m "feat: add job scraper integration"
git commit -m "fix: resolve Gemini API timeout"
git commit -m "test: add E2E tests for CV upload"
git commit -m "docs: update API documentation"
```

---

### **STEP 6: Push Feature Branch** (1 min)

```bash
# Option A: Use helper script
./scripts/gitflow.sh feature finish

# Option B: Manual
git push origin feature/my-feature-name
```

**Output will show:**
```
✅ Feature branch pushed
Next: Create PR at:
https://github.com/1AdrianM/job-fit-ai/compare/develop...feature/my-feature-name
```

---

### **STEP 7: Create Pull Request** (2 min)

**Go to GitHub:**
```
https://github.com/1AdrianM/job-fit-ai/compare/develop...feature/my-feature-name
```

**Or click "Compare & pull request" button on GitHub**

**Fill PR template:**
```markdown
## Description
Brief description of what this PR does

## Type
- [x] Feature
- [ ] Release
- [ ] Hotfix

## Testing
- [x] All Playwright tests pass locally
- [x] Manual testing completed
- [x] New tests added

## Checklist
- [x] Code follows style guidelines
- [x] Commit messages follow conventions
- [x] Tests added/updated
- [x] Documentation updated
- [x] Ready for review
```

**Base:** `develop` ← **Compare:** `feature/my-feature-name`

**Click "Create Pull Request"**

---

### **STEP 8: CI/CD Runs Automatically** (3-5 min)

**GitHub Actions will:**
1. ✅ Install dependencies (cached)
2. ✅ Run Ruff linting
3. ✅ Check code formatting
4. ✅ Run all 17 Playwright tests
5. ✅ Upload test reports
6. ✅ Report status on PR

**PR page will show:**
```
✅ Run Tests — Passed
✅ Code Quality — Passed

✓ All checks have passed
```

**If checks fail:**
- Click on failed check to see logs
- Fix the issue locally
- Commit and push again
- CI re-runs automatically

---

### **STEP 9: Review & Merge** (1 min)

**If you're solo:**
- Review your own changes
- Check the diff
- Verify CI passed
- Click **"Squash and merge"**

**If in team:**
- Request review from team member
- Address feedback
- Wait for approval
- Merge when approved

**After merge:**
```
✅ feature/my-feature-name merged into develop
✅ Branch can be deleted
```

**Click "Delete branch"**

---

### **STEP 10: Merge to Production** (2 min)

**When ready to deploy to production:**

```bash
# Create PR: develop → main
git checkout develop
git pull origin develop
```

**Go to GitHub:**
```
https://github.com/1AdrianM/job-fit-ai/compare/main...develop
```

**Create PR:**
- **Base:** `main` ← **Compare:** `develop`
- **Title:** `chore: release v1.x.x`
- **Description:** List of features/fixes included

**CI runs again on PR**

**When CI passes:**
- Click **"Squash and merge"**
- Merge to `main`

---

### **STEP 11: Auto-Deploy to Render** (5-10 min)

**Render detects push to `main`:**
```
🚀 Deploy started
   - Cloning from GitHub
   - Installing dependencies
   - Running build
   - Starting server
✅ Deploy live!
```

**Monitor deploy:**
```
https://dashboard.render.com
→ Select job-fit-ai
→ Click "Logs"
```

**When deploy succeeds:**
```
✅ Your feature is LIVE in production!
   https://job-fit-ai-1.onrender.com/
```

---

### **STEP 12: Verify Production** (2 min)

**Test live app:**
```bash
# Health check
curl https://job-fit-ai-1.onrender.com/health

# Or open in browser
https://job-fit-ai-1.onrender.com/
```

**Verify your feature works:**
- Click through the UI
- Test the new functionality
- Check browser console for errors
- Verify no breaking changes

**If something breaks:**
```bash
# Quick hotfix
git checkout main
git checkout -b hotfix/fix-critical-bug
# Fix the issue
git commit -m "fix: resolve critical production bug"
git push origin hotfix/fix-critical-bug
# Create PR: hotfix/fix-critical-bug → main
# Merge immediately
```

---

### **STEP 13: Sync Branches** (1 min)

**After production deploy, sync develop:**

```bash
git checkout develop
git pull origin develop
git merge main
git push origin develop
```

**Or let GitHub do it:**
Create PR: `main` → `develop` to sync back

---

## ⚡ **Quick Reference**

**Complete cycle in one shot:**

```bash
# 1. Start feature
./scripts/gitflow.sh feature start my-feature

# 2. Develop
# ... make changes ...

# 3. Test
npm test

# 4. Quality check
ruff check app/ --fix && ruff format app/

# 5. Commit
git add .
git commit -m "feat: add awesome feature"

# 6. Push & PR
./scripts/gitflow.sh feature finish
# Click the GitHub link to create PR

# 7. Wait for CI (auto)

# 8. Merge PR on GitHub

# 9. Create release PR: develop → main

# 10. Merge to main

# 11. Render auto-deploys (wait 5-10 min)

# 12. Verify production
curl https://job-fit-ai-1.onrender.com/health

# 13. Done! 🎉
```

---

## 🎯 **Typical Timeline**

| Step | Time | Notes |
|------|------|-------|
| Start feature | 2 min | Helper script or manual |
| Development | Variable | Depends on feature size |
| Write tests | 10-20 min | Per feature |
| Quality check | 2 min | Linting + formatting |
| Commit & push | 1 min | Conventional commits |
| Create PR | 2 min | Use template |
| CI/CD runs | 3-5 min | Automatic |
| Review & merge | 1 min | Solo or team |
| Merge to main | 2 min | Release PR |
| Render deploy | 5-10 min | Automatic |
| Verify production | 2 min | Manual check |
| **Total** | **~30-60 min** | For small feature |

---

## 🛠️ **Tools & Commands**

**Git Flow helper:**
```bash
./scripts/gitflow.sh feature start <name>
./scripts/gitflow.sh feature finish
./scripts/gitflow.sh status
```

**Local development:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Testing:**
```bash
npm test                      # Run all tests
npx playwright test --ui      # Visual mode
npx playwright test --debug   # Debug mode
```

**Code quality:**
```bash
ruff check app/              # Lint
ruff check app/ --fix        # Auto-fix
ruff format app/             # Format
```

**GitHub:**
```bash
git status                   # Check status
git log --oneline -10        # Recent commits
git branch -a                # All branches
```

---

## 📊 **Monitoring**

**GitHub Actions:**
```
https://github.com/1AdrianM/job-fit-ai/actions
```

**Render Dashboard:**
```
https://dashboard.render.com
```

**Production App:**
```
https://job-fit-ai-1.onrender.com/
```

**Health Endpoint:**
```
https://job-fit-ai-1.onrender.com/health
```

---

## 🆘 **Troubleshooting**

### **CI fails?**
1. Check GitHub Actions logs
2. Run tests locally: `npm test`
3. Fix issues
4. Push again

### **Deploy fails?**
1. Check Render logs
2. Verify environment variables
3. Check Python version (should be 3.12)
4. Rollback if needed (Render dashboard)

### **Production broken?**
1. Create hotfix branch immediately
2. Fix and deploy ASAP
3. Skip CI if critical (merge directly)
4. Post-mortem after fix

### **Merge conflicts?**
```bash
git checkout feature/my-feature
git fetch origin
git merge origin/develop
# Resolve conflicts
git commit
git push
```

---

## 🎓 **Best Practices**

1. ✅ **Small, focused features** (1-2 days max)
2. ✅ **Test before PR** (all tests must pass)
3. ✅ **Descriptive commits** (follow conventions)
4. ✅ **Review your own PR** (check the diff)
5. ✅ **Deploy often** (small releases are safer)
6. ✅ **Monitor production** (after each deploy)
7. ✅ **Keep branches synced** (pull often)
8. ✅ **Delete merged branches** (keep repo clean)

---

## 🚀 **Ready to Start?**

Pick your first feature and start the loop!

**Suggested first features:**
1. CV file upload (replace textarea)
2. Job URL scraping (paste link instead of text)
3. Email results functionality
4. PDF export of cover letter
5. Save/load analysis history

**Let's build! 🎯**
