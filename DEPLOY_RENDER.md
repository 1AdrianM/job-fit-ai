# Render Deployment Guide

## 🚀 Deploy to Render (Free Tier)

Render offers 750 hours/month free hosting - perfect for portfolio projects!

### Quick Deploy

**Step 1: Push to GitHub** (Already done! ✅)

**Step 2: Connect to Render**

1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Select **"1AdrianM/job-fit-ai"**
5. Click **"Connect"**

**Step 3: Configure Service**

**Basic Settings:**
- **Name:** `job-fit-ai`
- **Region:** Oregon (US West) - faster for LATAM
- **Branch:** `main`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Plan:** Free
- **Health Check Path:** `/health`

**Step 4: Add Environment Variables**

Click **"Environment"** tab and add:

```
GEMINI_API_KEY=your_api_key_here
DEBUG=False
HOST=0.0.0.0
DATABASE_URL=sqlite:///./job_fit.db
```

**Step 5: Deploy**

Click **"Create Web Service"**

Render will:
1. ✅ Clone your repo
2. ✅ Install dependencies
3. ✅ Start your app
4. ✅ Give you a public URL

---

## 🌐 Your App URL

After deployment, your app will be available at:

```
https://job-fit-ai-XXXXX.onrender.com
```

(Render will show you the exact URL in the dashboard)

---

## 🔄 Auto-Deployment

Once connected, Render automatically deploys when you push to `main`:

```bash
git push origin main
# 🚀 Render automatically deploys!
```

---

## 📊 Monitoring

**View Logs:**
```
Render Dashboard → Your Service → Logs
```

**Check Health:**
```
https://your-app.onrender.com/health
```

**View Metrics:**
```
Render Dashboard → Your Service → Metrics
```

---

## 🐛 Troubleshooting

### App not starting?

**Check logs:**
- Dashboard → Logs
- Look for errors in startup

**Common issues:**

1. **Missing GEMINI_API_KEY**
   - Add it in Environment tab
   - Redeploy

2. **Port binding error**
   - Use `--port $PORT` (Render provides this)
   - Don't hardcode port 8000

3. **Dependencies error**
   - Check requirements.txt
   - Make sure all packages are listed

### App sleeps after inactivity?

**Free tier limitation:**
- Apps sleep after 15 min inactivity
- Wake up on first request (takes ~30 seconds)

**Solutions:**
- Upgrade to paid tier ($7/month for always-on)
- Use a cron job to ping your app every 10 minutes
- Accept the cold start (fine for portfolio projects)

---

## 🎯 Next Steps

After deployment:

1. ✅ Test your live app
2. ✅ Update README with live URL
3. ✅ Add to LinkedIn/portfolio
4. ✅ Share with potential employers

---

## 💰 Free Tier Limits

Render Free Tier includes:

- ✅ 750 hours/month (plenty for one app)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Automatic deploys from GitHub
- ⚠️ Apps sleep after 15 min inactivity
- ⚠️ 100GB bandwidth/month

Perfect for portfolio projects and demos!

---

## 🔐 Security Notes

**Never commit secrets:**
- ✅ Use Render's Environment Variables
- ✅ `.env` is gitignored
- ✅ Secrets are encrypted at rest

**Production checklist:**
- ✅ Set `DEBUG=False`
- ✅ Use strong API keys
- ✅ Enable CORS only for your domain
- ✅ Monitor logs for suspicious activity

---

## 📞 Support

Having issues?

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** https://github.com/1AdrianM/job-fit-ai/issues
- **Email:** adrianbatista025@gmail.com

---

## 🎉 You're Live!

Once deployed, your Job Fit AI is accessible worldwide at:

```
https://job-fit-ai-XXXXX.onrender.com
```

Share it on LinkedIn, add it to your resume, and use it in your job search! 🚀
