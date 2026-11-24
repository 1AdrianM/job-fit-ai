# 🚀 Render Setup - Step by Step

## ⚠️ Current Issue
Render is using Python 3.14 instead of 3.12, causing pydantic-core build errors.

## ✅ Solution: Delete and recreate service

### Step 1: Delete existing service

1. Go to: https://dashboard.render.com
2. Click on your `job-fit-ai` service
3. Click **"Settings"** tab
4. Scroll to bottom
5. Click **"Delete Web Service"**
6. Type the service name to confirm
7. Click **"Delete"**

### Step 2: Create new service (will use runtime.txt)

1. Click **"New +"** → **"Web Service"**

2. Click **"Build and deploy from a Git repository"**

3. Select repository: **`1AdrianM/job-fit-ai`**

4. Click **"Connect"**

5. **Configuration:**
   ```
   Name: job-fit-ai
   Region: Oregon (US West)
   Branch: main
   
   Runtime: Python (auto-detected)
   
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   
   Plan: Free
   ```

6. **Environment Variables** (click "Advanced"):
   
   Click **"Add Environment Variable"** for each:
   
   ```
   Key: GEMINI_API_KEY
   Value: (paste your Gemini API key)
   
   Key: DEBUG
   Value: False
   
   Key: HOST
   Value: 0.0.0.0
   
   Key: DATABASE_URL
   Value: sqlite:///./job_fit.db
   ```

7. **Click "Create Web Service"**

8. **Wait 5-10 minutes** for first deploy

---

## ✅ Verification

After deploy succeeds:

1. **Check Python version in logs:**
   Look for: `Using Python version 3.12.0`

2. **Test health endpoint:**
   ```
   https://your-app.onrender.com/health
   ```
   
   Should return:
   ```json
   {"status": "healthy", "app": "Job Fit AI"}
   ```

3. **Test homepage:**
   ```
   https://your-app.onrender.com
   ```
   
   Should load the Job Fit AI interface

---

## 🔑 Get your Gemini API Key

If you don't have it:

1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)
4. Use it in Render environment variables

---

## 📝 Notes

- **runtime.txt** specifies Python 3.12.0
- **render.yaml** also specifies pythonVersion: 3.12.0
- Render will auto-detect both and use Python 3.12
- Free tier: app sleeps after 15 min inactivity (~30s wake time)

---

## 🆘 If deploy still fails

Check logs for:

1. **Missing GEMINI_API_KEY:**
   ```
   KeyError: 'gemini_api_key'
   ```
   Solution: Add it in Environment Variables

2. **Port binding error:**
   ```
   Error binding to port
   ```
   Solution: Verify start command uses `$PORT`

3. **Still using Python 3.14:**
   Delete service and recreate from scratch

---

## ✅ Ready for development loop

Once deploy succeeds, we'll set up:

1. **Feature development** on `feature/*` branches
2. **Local testing** with Playwright
3. **PR to develop** → CI runs
4. **Merge to main** → Auto-deploy to Render
5. **Verify production**

Ready to start the loop! 🚀
