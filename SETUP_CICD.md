# Setting up GitHub Actions CI/CD

GitHub Actions workflows are ready but need to be added manually due to token scope limitations.

## Step 1: Configure GitHub Secrets

Go to: `https://github.com/1AdrianM/job-fit-ai/settings/secrets/actions`

Add these secrets:

### Required Secrets

1. **GEMINI_API_KEY** (Required for CI tests)
   - Value: Your Google Gemini API key
   - Get it from: https://makersuite.google.com/app/apikey

### Optional Secrets (for deployment)

2. **RAILWAY_TOKEN** (For auto-deployment)
   - Create a Railway project: https://railway.app
   - Get token from: Railway Dashboard → Account Settings → Tokens
   - Value: Your Railway token

3. **GIST_TOKEN** (For dynamic test badges)
   - Create at: https://github.com/settings/tokens/new
   - Scopes needed: `gist`
   - Value: Your generated token

4. **GIST_ID** (For badge storage)
   - Create a secret gist: https://gist.github.com/
   - Name: `job-fit-ai-tests.json`
   - Content: `{}`
   - Value: The gist ID from the URL (e.g., `abc123...`)

## Step 2: Add Workflow Files

The workflow files are in `.github/workflows/` but need workflow scope to push.

### Option A: Add via GitHub Web UI (Recommended)

1. Go to: `https://github.com/1AdrianM/job-fit-ai`
2. Click: **Add file** → **Create new file**
3. Path: `.github/workflows/ci.yml`
4. Copy content from local `.github/workflows/ci.yml`
5. Commit: "ci: add CI pipeline"
6. Repeat for `.github/workflows/deploy.yml`

### Option B: Update gh CLI token with workflow scope

```bash
# 1. Login with workflow scope
gh auth login --scopes workflow

# 2. Push the workflows
git add .github/workflows/
git commit -m "ci: add GitHub Actions workflows"
git push origin main
```

## Step 3: Verify CI Pipeline

After adding workflows:

1. Go to: `https://github.com/1AdrianM/job-fit-ai/actions`
2. You should see the CI pipeline running
3. First run will fail if GEMINI_API_KEY is not set
4. Add the secret and re-run the workflow

## Step 4: Set up Railway Deployment (Optional)

1. Create Railway project: https://railway.app
2. Connect to your GitHub repo
3. Add environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `DEBUG`: `False`
   - `HOST`: `0.0.0.0`
   - `PORT`: `$PORT` (Railway provides this)
4. Deploy!

## Verification

✅ CI Pipeline badge shows up in README  
✅ Tests run on every push  
✅ Deployment triggers on main branch push  

## Troubleshooting

### "refusing to allow an OAuth App to create or update workflow"
- Your token doesn't have `workflow` scope
- Use Option A (Web UI) or Option B (re-login) above

### Tests failing in CI
- Check `GEMINI_API_KEY` secret is set
- Verify the secret value is correct
- Check Actions logs for specific errors

### Deployment not triggering
- Verify `RAILWAY_TOKEN` secret is set
- Check Railway project is connected to repo
- Review deploy.yml workflow file

## Next Steps

After CI/CD is set up:

1. Make a small change to trigger CI
2. Watch the Actions tab to see tests run
3. Verify badges update in README
4. Set up Railway deployment for production

## Support

Having issues? Open an issue or contact:
- GitHub: [@1AdrianM](https://github.com/1AdrianM)
- Email: adrianbatista025@gmail.com
