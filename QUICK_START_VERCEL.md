# ⚡ Quick Start: Deploy CropGPT to Vercel in 15 Minutes

This is the fastest way to get your app live!

## 🎯 What We're Doing

1. **Backend** → Railway (5 minutes)
2. **Frontend** → Vercel (5 minutes)  
3. **Connect & Test** (5 minutes)

---

## Step 1: Deploy Backend to Railway (5 min)

### 1.1 Sign Up
- Go to https://railway.app
- Click "Login with GitHub"
- Authorize Railway

### 1.2 Create Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose: `BishalJena/CropGPT`

### 1.3 Add Services
Railway will detect your backend. Click on it and:

**Settings:**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### 1.4 Add MongoDB
- Click "+ New" → "Database" → "MongoDB"
- Railway auto-configures it

### 1.5 Add Redis
- Click "+ New" → "Database" → "Redis"
- Railway auto-configures it

### 1.6 Add Environment Variables

Go to Backend Service → Variables → Add:

```env
# Required
CEREBRAS_API_KEY=your_key_here
JWT_SECRET=your_32_char_secret_here

# MongoDB & Redis (auto-filled by Railway)
MONGO_URL=${{MongoDB.MONGO_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
DB_NAME=farmchat

# CORS (update after Vercel deployment)
CORS_ORIGINS=*

# Optional
OPENROUTER_API_KEY=your_key_here
DEEPGRAM_API_KEY=your_key_here
EXA_API_KEY=your_key_here
DATAGOVIN_API_KEY=your_key_here
MCP_GATEWAY_URL=http://165.232.190.215:8811

ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Generate JWT_SECRET:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 1.7 Get Backend URL
- Go to Settings → Domains
- Copy URL: `https://cropgpt-backend-production.up.railway.app`
- **Save this URL!**

### 1.8 Deploy
- Railway deploys automatically
- Wait 2-3 minutes
- Check: `https://your-backend-url/api/health`

✅ **Backend Done!**

---

## Step 2: Update Frontend Config

Before deploying to Vercel, create this file:

**File**: `frontend/.env.production`
```env
REACT_APP_BACKEND_URL=https://your-backend-url.railway.app
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=production
```

**Replace** `your-backend-url.railway.app` with your actual Railway URL!

---

## Step 3: Deploy Frontend to Vercel (5 min)

### 3.1 Commit Your Changes
```bash
# Make sure vercel.json and other files are committed
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

### 3.2 Sign Up to Vercel
- Go to https://vercel.com/signup
- Click "Continue with GitHub"
- Authorize Vercel

### 3.3 Import Project
- Click "Add New..." → "Project"
- Import `BishalJena/CropGPT`

### 3.4 Configure Build Settings
```
Framework Preset: Other
Root Directory: ./
Build Command: cd frontend && npm install --legacy-peer-deps && npm run build
Output Directory: frontend/build
Install Command: cd frontend && npm install --legacy-peer-deps
```

### 3.5 Add Environment Variables

In Vercel dashboard, add these:

```env
REACT_APP_BACKEND_URL=https://your-backend-url.railway.app
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=production
REACT_APP_ENABLE_VOICE=true
REACT_APP_ENABLE_WORKFLOWS=true
REACT_APP_ENABLE_MARKETPLACE=true
REACT_APP_ENABLE_SCHEMES=true
```

**Replace** with your Railway backend URL!

### 3.6 Deploy
- Click "Deploy"
- Wait 3-5 minutes
- Get URL: `https://cropgpt.vercel.app`

✅ **Frontend Done!**

---

## Step 4: Connect Backend & Frontend (5 min)

### 4.1 Update Backend CORS

Go to Railway → Backend Service → Variables:

**Update** `CORS_ORIGINS`:
```
https://cropgpt.vercel.app,https://cropgpt-*.vercel.app
```

Railway will auto-redeploy (1-2 min).

### 4.2 Test Your App

Visit: `https://cropgpt.vercel.app`

**Test Flow:**
1. ✅ Register new user
2. ✅ Login
3. ✅ Send message: "What is the current price of wheat in Punjab?"
4. ✅ Get AI response

---

## 🎉 You're Live!

Your app is now deployed:
- **Frontend**: https://cropgpt.vercel.app
- **Backend**: https://your-backend.railway.app
- **Database**: MongoDB on Railway
- **Cache**: Redis on Railway

---

## 🔧 Troubleshooting

### ❌ CORS Error
**Problem**: Frontend can't connect to backend
**Fix**: 
1. Check `CORS_ORIGINS` in Railway includes your Vercel URL
2. Make sure it's deployed (check Railway logs)

### ❌ Build Failed (Vercel)
**Problem**: npm install fails
**Fix**:
```bash
# Test locally first
cd frontend
npm install --legacy-peer-deps
npm run build
```

### ❌ Build Failed (Railway)
**Problem**: pip install fails
**Fix**:
1. Check Railway logs
2. Verify requirements.txt
3. Check Python version (should use 3.8+)

### ❌ API Not Working
**Problem**: 500 errors from backend
**Fix**:
1. Check Railway logs for errors
2. Verify environment variables
3. Check MongoDB connection

---

## 💡 Next Steps

### Add Custom Domain
**Vercel:**
1. Settings → Domains
2. Add `cropgpt.com`
3. Update DNS

**Railway:**
1. Settings → Domains
2. Add `api.cropgpt.com`
3. Update frontend URL

### Enable Analytics
```env
# In Vercel
REACT_APP_GA_TRACKING_ID=G-XXXXXXXXXX
```

### Set Up Monitoring
- Vercel: Built-in analytics
- Railway: Built-in metrics
- Optional: Add Sentry for error tracking

---

## 📊 Cost Summary

### Free Tier
- **Vercel**: Free forever (100GB bandwidth)
- **Railway**: $5 credit/month (good for testing)

### Production (~$15-20/month)
- **Vercel**: Free or $20/month (Pro)
- **Railway**: $10-15/month (backend + databases)

---

## 🆘 Need Help?

1. **Railway Issues**: Check Railway docs or Discord
2. **Vercel Issues**: Check Vercel docs or Discord  
3. **App Issues**: Check application logs

**Logs:**
- Railway: Service → Logs tab
- Vercel: Project → Deployments → View Function Logs

---

## ✅ Final Checklist

- [ ] Railway backend deployed
- [ ] MongoDB added
- [ ] Redis added
- [ ] Environment variables set
- [ ] Backend URL copied
- [ ] Frontend env updated
- [ ] Changes pushed to GitHub
- [ ] Vercel frontend deployed
- [ ] Vercel env variables set
- [ ] CORS updated
- [ ] App tested end-to-end

---

**🎉 Congratulations! Your CropGPT is live! 🚀🌾**

Share it with farmers and start helping them grow better crops! 🌱
