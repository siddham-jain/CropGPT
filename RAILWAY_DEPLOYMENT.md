# 🚂 Railway Deployment Guide for CropGPT Backend

Step-by-step guide to deploy your FastAPI backend on Railway.

## 🎯 Why Railway for Backend?

- ✅ **Easy Python deployment** (auto-detects FastAPI)
- ✅ **Built-in MongoDB and Redis** (no external setup)
- ✅ **Automatic HTTPS** (SSL certificates included)
- ✅ **Environment variables** (secure secret management)
- ✅ **Auto-deploy from GitHub** (CI/CD built-in)
- ✅ **$5 free credit** per month

## 📋 Prerequisites

1. GitHub account with repository pushed
2. Railway account (sign up at https://railway.app)
3. API keys ready (Cerebras, OpenRouter, Deepgram, etc.)

---

## Part 1: Create Railway Account

1. Go to https://railway.app
2. Click "Start a New Project"
3. Login with GitHub
4. Authorize Railway to access your repositories

---

## Part 2: Deploy Backend Service

### Step 1: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: `BishalJena/CropGPT`
4. Railway will auto-detect your services

### Step 2: Configure Backend Service

1. **Select backend directory**:
   - Click on the detected service
   - Settings → Root Directory: `backend`

2. **Configure build settings**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

3. **Add environment variables** (Settings → Variables):

   ```env
   # Database (Railway will provide these)
   MONGO_URL=${{MongoDB.MONGO_URL}}
   DB_NAME=farmchat
   
   # Redis (Railway will provide these)
   REDIS_URL=${{Redis.REDIS_URL}}
   
   # Authentication
   JWT_SECRET=<generate-a-strong-random-string-32-chars>
   JWT_EXPIRATION_HOURS=24
   
   # AI Service API Keys
   CEREBRAS_API_KEY=<your-cerebras-api-key>
   OPENROUTER_API_KEY=<your-openrouter-api-key>
   DEEPGRAM_API_KEY=<your-deepgram-api-key>
   
   # External API Keys
   EXA_API_KEY=<your-exa-api-key>
   DATAGOVIN_API_KEY=<your-datagovin-api-key>
   
   # MCP Gateway (Railway internal or external)
   MCP_GATEWAY_URL=http://mcp-gateway.railway.internal:10000
   # MCP_GATEWAY_TOKEN=<optional-bearer-token>
   
   # CORS - Add your Vercel URL here after frontend deployment
   CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
   
   # Server Configuration
   PORT=$PORT
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

   **Generate strong JWT_SECRET**:
   ```bash
   # Run this in your terminal
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Step 3: Add MongoDB Database

1. In your Railway project, click **"New"** → **"Database"** → **"Add MongoDB"**
2. Railway will automatically:
   - Create MongoDB instance
   - Generate connection URL
   - Add `MONGO_URL` to your environment
3. No additional configuration needed!

### Step 4: Add Redis Cache

1. Click **"New"** → **"Database"** → **"Add Redis"**
2. Railway will automatically:
   - Create Redis instance
   - Generate connection URL
   - Add `REDIS_URL` to your environment
3. No additional configuration needed!

### Step 5: Deploy MCP Gateway (Optional)

1. Click **"New"** → **"Empty Service"**
2. Name it: `mcp-gateway`
3. Settings → Root Directory: `fs-gate`
4. Build Command: `npm install`
5. Start Command: `npm start`
6. Environment Variables:
   ```env
   NODE_ENV=production
   PORT=10000
   DATAGOVIN_API_KEY=<your-datagovin-api-key>
   EXA_API_KEY=<your-exa-api-key>
   ```

### Step 6: Get Your Backend URL

1. Go to backend service
2. Settings → Domains
3. Railway provides: `https://your-backend.railway.app`
4. **Copy this URL** for frontend configuration

---

## Part 3: Configure Railway Settings

### Enable Auto-Deploy

1. Settings → GitHub → Connect Repository
2. Enable "Auto-deploy on push to main"
3. Now every git push automatically deploys!

### Set Up Health Checks

1. Settings → Health Checks
2. HTTP Path: `/api/health`
3. Interval: 30 seconds
4. Timeout: 10 seconds

### Configure Resources (if needed)

1. Settings → Resources
2. Default is usually sufficient
3. Can upgrade if you need more:
   - Memory: 512MB → 1GB
   - CPU: 0.5 vCPU → 1 vCPU

---

## Part 4: Test Your Deployment

### Test Health Endpoint
```bash
curl https://your-backend.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "mcp_gateway": "healthy"
  }
}
```

### Test API Documentation
```bash
# Visit in browser
https://your-backend.railway.app/docs
```

### Test Authentication
```bash
# Register a user
curl -X POST https://your-backend.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

---

## Part 5: Update Frontend Configuration

Now that backend is deployed, update your frontend:

### Option A: Update `.env.production`
```env
REACT_APP_BACKEND_URL=https://your-backend.railway.app
```

### Option B: Update in Vercel Dashboard
1. Go to Vercel project
2. Settings → Environment Variables
3. Edit `REACT_APP_BACKEND_URL`
4. Set to: `https://your-backend.railway.app`
5. Redeploy frontend

---

## Part 6: Update CORS Settings

Add your Vercel URL to backend CORS:

1. Go to Railway → Backend Service → Variables
2. Update `CORS_ORIGINS`:
   ```
   https://your-app.vercel.app,https://your-app-*.vercel.app
   ```
3. Railway will auto-redeploy

---

## 📊 Monitoring & Logs

### View Logs
1. Click on backend service
2. Go to "Logs" tab
3. Real-time logs streaming
4. Filter by severity: Info, Warning, Error

### View Metrics
1. Click on backend service
2. Go to "Metrics" tab
3. See:
   - CPU usage
   - Memory usage
   - Network traffic
   - Request count

### Set Up Alerts
1. Settings → Notifications
2. Add email/Slack webhook
3. Get notified on:
   - Deployment failures
   - Service crashes
   - High resource usage

---

## 💰 Cost Estimation

### Free Tier ($5 credit/month)
- ✅ Good for testing and low-traffic apps
- 500MB RAM per service
- Shared CPU
- Includes: Backend + MongoDB + Redis

### Paid Tier (Usage-based)
- Backend: ~$5-10/month
- MongoDB: ~$3-5/month
- Redis: ~$2-3/month
- **Total**: ~$10-18/month for production

### Cost Optimization Tips
1. **Use Railway's free tier** for development
2. **Upgrade only when needed** (monitor usage)
3. **Use MongoDB Atlas free tier** instead of Railway MongoDB
4. **Use Redis Cloud free tier** instead of Railway Redis

---

## 🔒 Security Best Practices

### 1. Secure Secrets
```bash
# Never commit these to git
# Use Railway environment variables

# Generate strong secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. CORS Configuration
```env
# Only allow your domains
CORS_ORIGINS=https://your-app.vercel.app,https://api.cropgpt.com
```

### 3. Rate Limiting
```python
# Already implemented in your FastAPI backend
# Adjust in server.py if needed
```

### 4. HTTPS Only
```env
# Railway provides HTTPS by default
# Enforce HTTPS in production
```

---

## 🚀 Deployment Workflow

```mermaid
graph LR
    A[Code Change] --> B[Git Push]
    B --> C[GitHub]
    C --> D[Railway Auto-Deploy]
    D --> E[Build]
    E --> F[Test]
    F --> G[Deploy]
    G --> H[Health Check]
    H --> I[Live!]
```

---

## 🔧 Troubleshooting

### Build Fails
**Issue**: Dependency installation fails
**Solution**:
```bash
# Test locally first
cd backend
pip install -r requirements.txt

# Check requirements.txt for conflicts
# Remove version pins if needed
```

### Database Connection Fails
**Issue**: Cannot connect to MongoDB
**Solution**:
```bash
# Check MONGO_URL in Railway variables
# Format: mongodb://username:password@host:port/database

# Test connection
python -c "from pymongo import MongoClient; print(MongoClient('$MONGO_URL').server_info())"
```

### CORS Errors
**Issue**: Frontend can't connect to backend
**Solution**:
```env
# Add all possible Vercel URLs
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-*.vercel.app,https://*.vercel.app
```

### High Memory Usage
**Issue**: Service keeps restarting
**Solution**:
1. Check Metrics → Memory usage
2. Settings → Resources → Increase memory
3. Or optimize code for memory efficiency

---

## 📚 Additional Resources

- **Railway Docs**: https://docs.railway.app
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **MongoDB Atlas**: https://www.mongodb.com/atlas
- **Redis Cloud**: https://redis.com/cloud/

---

## ✅ Deployment Checklist

- [ ] Railway account created
- [ ] Backend service deployed
- [ ] MongoDB database added
- [ ] Redis cache added
- [ ] Environment variables configured
- [ ] MCP Gateway deployed (optional)
- [ ] Health endpoint tested
- [ ] Backend URL copied
- [ ] CORS configured
- [ ] Auto-deploy enabled
- [ ] Monitoring set up
- [ ] Frontend updated with backend URL

---

## 🎉 Success!

Your backend is now live on Railway at:
```
https://your-backend.railway.app
```

**Next Steps**:
1. Deploy frontend to Vercel (see VERCEL_DEPLOYMENT.md)
2. Update frontend environment variables
3. Test end-to-end functionality
4. Set up custom domain (optional)
5. Configure monitoring and alerts

**Happy Deploying! 🚂🚀**
