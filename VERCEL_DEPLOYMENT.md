# 🚀 Vercel Deployment Guide for CropGPT

This guide will help you deploy your CropGPT application with **Frontend on Vercel** and **Backend on Railway/Render**.

## 📋 Prerequisites

- GitHub account with your repository pushed
- Vercel account (free tier is sufficient)
- Railway/Render account for backend (or keep existing DigitalOcean setup)

## 🎯 Deployment Architecture

```
Frontend (Vercel) → Backend API (Railway/Render/DigitalOcean)
                   → MongoDB Atlas (Cloud Database)
                   → Redis Cloud (Cache)
```

## Part 1: Deploy Backend to Railway (Recommended)

### Option A: Railway Deployment (Easiest)

1. **Sign up for Railway**: https://railway.app
2. **Create New Project** → **Deploy from GitHub repo**
3. **Select your repository**: `BishalJena/CropGPT`
4. **Add services**:
   - Backend API (from `/backend`)
   - MCP Gateway (from `/fs-gate`)
   - MongoDB (Railway provides this)
   - Redis (Railway provides this)

#### Configure Backend Service:
```bash
# Railway will auto-detect Python, but add these settings:

# Build Command
cd backend && pip install -r requirements.txt

# Start Command
cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
```

#### Environment Variables for Backend on Railway:
```env
# Database
MONGO_URL=${{MongoDB.MONGO_URL}}  # Railway auto-provides this
DB_NAME=farmchat

# Redis
REDIS_URL=${{Redis.REDIS_URL}}  # Railway auto-provides this

# Authentication
JWT_SECRET=<generate-strong-secret-key>

# AI Services
CEREBRAS_API_KEY=<your-cerebras-api-key>
OPENROUTER_API_KEY=<your-openrouter-api-key>
DEEPGRAM_API_KEY=<your-deepgram-api-key>

# MCP Gateway
MCP_GATEWAY_URL=http://mcp-gateway:10000  # Internal Railway URL
MCP_GATEWAY_TOKEN=<optional-bearer-token>

# API Keys
EXA_API_KEY=<your-exa-api-key>
DATAGOVIN_API_KEY=<your-datagovin-api-key>

# CORS (add your Vercel domain once deployed)
CORS_ORIGINS=https://your-app.vercel.app,https://cropgpt.vercel.app

# Server
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=INFO
```

5. **Get Backend URL**: After deployment, Railway provides a URL like:
   - `https://your-backend.railway.app`
   - Copy this URL for frontend configuration

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Your Repository

The necessary files have been created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `.vercelignore` - Files to exclude
- ✅ `frontend/.env.production` - Production environment variables

### Step 2: Update Frontend Environment Variables

Edit `frontend/.env.production`:
```env
# Update with your Railway backend URL
REACT_APP_BACKEND_URL=https://your-backend.railway.app
```

### Step 3: Commit and Push Changes

```bash
# Add new configuration files
git add vercel.json .vercelignore frontend/.env.production VERCEL_DEPLOYMENT.md

# Commit changes
git commit -m "Add Vercel deployment configuration"

# Push to GitHub
git push origin main
```

### Step 4: Deploy to Vercel

#### Method 1: Vercel Dashboard (Recommended)

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**:
   - Click "Import Project"
   - Connect your GitHub account
   - Select repository: `BishalJena/CropGPT`
3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: Leave as `./` (vercel.json handles this)
   - **Build Command**: `cd frontend && npm install --legacy-peer-deps && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && npm install --legacy-peer-deps`

4. **Environment Variables** (Add these in Vercel dashboard):
   ```
   REACT_APP_BACKEND_URL=https://your-backend.railway.app
   REACT_APP_VERSION=1.0.0
   REACT_APP_ENVIRONMENT=production
   REACT_APP_ENABLE_VOICE=true
   REACT_APP_ENABLE_WORKFLOWS=true
   REACT_APP_ENABLE_MARKETPLACE=true
   REACT_APP_ENABLE_SCHEMES=true
   ```

5. **Deploy**: Click "Deploy" button
6. **Wait for deployment**: Vercel will build and deploy (2-5 minutes)
7. **Get your URL**: `https://your-app.vercel.app`

#### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# Follow prompts:
# - Link to existing project: No
# - Project name: cropgpt
# - Directory: ./
# - Override build settings: No

# Deploy to production
vercel --prod
```

---

## Part 3: Update Backend CORS Settings

After getting your Vercel URL, update backend CORS:

### On Railway:
1. Go to your backend service
2. Add environment variable:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://cropgpt.vercel.app
   ```
3. Redeploy backend

### On your existing server:
Update `backend/.env`:
```env
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

---

## Part 4: Configure Custom Domain (Optional)

### On Vercel:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed

### On Railway (Backend):
1. Go to Settings → Domains
2. Add custom domain like `api.cropgpt.com`
3. Update frontend `REACT_APP_BACKEND_URL`

---

## 🧪 Testing Deployment

### Test Frontend:
```bash
# Visit your Vercel URL
https://your-app.vercel.app

# Test authentication
# Register a new user
# Try sending a farming query
```

### Test Backend Connection:
```bash
# Check backend health
curl https://your-backend.railway.app/api/health

# Test CORS
curl -H "Origin: https://your-app.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://your-backend.railway.app/api/chat
```

---

## 📊 Monitoring & Logs

### Vercel:
- **Deployments**: https://vercel.com/dashboard
- **Analytics**: Project → Analytics
- **Logs**: Project → Deployments → View Function Logs

### Railway:
- **Logs**: Service → Logs tab
- **Metrics**: Service → Metrics tab
- **Deployments**: Service → Deployments tab

---

## 🔧 Troubleshooting

### Issue: Build fails on Vercel

**Solution**: Check build logs, ensure all dependencies are in `package.json`:
```bash
cd frontend
npm install --legacy-peer-deps
npm run build  # Test locally first
```

### Issue: CORS errors

**Solution**: Verify backend CORS_ORIGINS includes your Vercel URL:
```env
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-*.vercel.app
```

### Issue: API calls failing

**Solution**: Check `REACT_APP_BACKEND_URL` in Vercel environment variables:
```bash
# In Vercel dashboard
Settings → Environment Variables → Check REACT_APP_BACKEND_URL
```

### Issue: Environment variables not working

**Solution**: Redeploy after adding environment variables:
```bash
# In Vercel dashboard
Deployments → Latest Deployment → Redeploy
```

---

## 💰 Cost Estimates

### Free Tier:
- **Vercel**: Free (includes 100GB bandwidth)
- **Railway**: $5 credit/month (backend ~$10-15/month)
- **MongoDB Atlas**: Free tier (512MB)
- **Redis Cloud**: Free tier (30MB)

### Recommended Tier (~$20/month):
- **Vercel Pro**: $20/month (more bandwidth)
- **Railway**: $15-20/month (backend + services)
- **MongoDB Atlas**: $9/month (2GB)
- **Redis Cloud**: Free tier sufficient

---

## 🚦 Deployment Checklist

- [ ] Backend deployed to Railway/Render
- [ ] MongoDB and Redis configured
- [ ] Backend environment variables set
- [ ] Backend URL copied
- [ ] Frontend `.env.production` updated
- [ ] Changes pushed to GitHub
- [ ] Frontend deployed to Vercel
- [ ] Frontend environment variables set
- [ ] CORS configured on backend
- [ ] Test user registration
- [ ] Test chat functionality
- [ ] Test voice features
- [ ] Custom domain configured (optional)

---

## 📚 Alternative Backend Hosting Options

### Option B: Render.com
```bash
# Similar to Railway, but with simpler pricing
# Free tier available for testing
# Automatic deploys from GitHub
```

### Option C: Keep DigitalOcean
```bash
# Keep your existing backend on DigitalOcean
# Only deploy frontend to Vercel
# Update REACT_APP_BACKEND_URL to your DigitalOcean URL
```

### Option D: Vercel Serverless (Advanced, Not Recommended)
```bash
# Would require significant backend refactoring
# FastAPI → Individual serverless functions
# Not recommended for this complex application
```

---

## 🎉 Success!

Once deployed, your application will be live:
- **Frontend**: `https://your-app.vercel.app` (Global CDN, fast)
- **Backend**: `https://your-backend.railway.app` (Scalable API)
- **Database**: MongoDB Atlas (Cloud-hosted)
- **Cache**: Redis Cloud (Fast caching)

### Next Steps:
1. Set up monitoring (Sentry, LogRocket)
2. Configure analytics (Google Analytics)
3. Add custom domain
4. Set up CI/CD pipelines
5. Configure staging environment

---

## 💬 Support

If you encounter issues:
- Check Vercel build logs
- Check Railway/Render deployment logs
- Verify environment variables
- Test backend health endpoint
- Check CORS configuration

**Happy Deploying! 🚀🌾**
