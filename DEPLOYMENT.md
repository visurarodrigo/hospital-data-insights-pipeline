# 🚀 Deployment Guide

## Current Deployment Status

✅ **Frontend**: Deployed on Firebase Hosting (Modern SaaS UI with Dark Mode)  
🖥️ **Backend**: Running locally on port 3000 (not yet deployed to cloud)

---

## Firebase Hosting (Frontend) - ✅ DEPLOYED

### Prerequisites
- Node.js installed (for Firebase CLI)
- Firebase account
- Firebase project created

### Steps

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   firebase --version
   ```

2. **Login to Firebase**
   ```bash
   firebase login
   ```

3. **Deploy**
   ```bash
   firebase deploy --only hosting
   ```

Your frontend is live at: `https://hospital-insights-c9c40.web.app`

**What's Deployed:**
- Modern SaaS-style UI with design system
- Dark mode support with theme toggle
- Fully responsive layout (mobile/tablet/desktop)
- Toast notifications and loading states
- All 4 dashboard pages (Overview, OPD, Inpatient, AI Risk)
- Interactive visualizations with Chart.js

---

## Backend Deployment (Optional - Not Yet Implemented)

The backend currently runs locally for development. If you want to deploy it to production, here are the available options:

### Google Cloud Run (Backend API)

### Prerequisites
- Google Cloud account with billing enabled
- gcloud CLI installed
- Docker installed (optional, can use Cloud Build)

### Option 1: Deploy with Cloud Build (Easier)

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Deploy directly from source
gcloud run deploy hospital-api \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300
```

### Option 2: Deploy with Docker

```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/hospital-api .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/hospital-api

# Deploy to Cloud Run
gcloud run deploy hospital-api \
  --image gcr.io/YOUR_PROJECT_ID/hospital-api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

### After Deployment

1. Note your Cloud Run URL (e.g., `https://hospital-api-xxxxx-uc.a.run.app`)
2. Update `frontend/dashboard.js`:
   ```javascript
   const API_BASE_URL = 'https://your-cloud-run-url.com';
   ```
   (Currently set to: `http://localhost:3000` for local development)
3. Redeploy frontend:
   ```bash
   firebase deploy --only hosting
   ```

---

## Alternative: Railway.app (Simplest)

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `hospital-data-insights-pipeline` repo
5. Railway auto-detects Python and deploys
6. Add environment variable: `PORT=8000`
7. Your API will be at: `https://your-app.railway.app`

---

## Environment Variables (Production)

For production deployment, consider setting:

```bash
# Cloud Run
gcloud run services update hospital-api \
  --set-env-vars="DB_PATH=/tmp/hospital_warehouse.db" \
  --set-env-vars="MODEL_DIR=/app/models"
```

---

## Important Notes

### Data & Models
- Generated data and models are ignored in Docker
- Options:
  1. **Run pipeline in Cloud Run** (via startup script)
  2. **Use Cloud Storage** for data/models
  3. **Bake into image** (remove from .dockerignore)

### CORS Configuration
Already configured in `backend/api.py`:
```python
allow_origins=["*"]  # Update to specific domain in production
```

For production, update to:
```python
allow_origins=["https://your-project-id.web.app"]
```

---

## Cost Estimates

### Firebase Hosting
- **Spark Plan (Free)**: 10 GB storage, 360 MB/day bandwidth
- Perfect for this project

### Cloud Run
- **Free Tier**: 2 million requests/month, 360,000 GB-seconds
- Estimated: **$0-5/month** for low traffic

### Railway
- **Free Tier**: $5 credit/month
- **Hobby Plan**: $5/month

---

## Monitoring

### Firebase Console
- View hosting analytics
- Monitor bandwidth usage

### Cloud Run Console
- View request logs
- Monitor latency, errors
- Auto-scaling metrics

---

## Quick Deploy Commands

```bash
# Frontend only
firebase deploy --only hosting

# Backend only (Cloud Run)
gcloud run deploy hospital-api --source .

# Both
firebase deploy && gcloud run deploy hospital-api --source .
```

---

## Troubleshooting

**Frontend shows "API Offline"**
- Check API_BASE_URL in dashboard.js (Line 11)
- Verify Cloud Run service is running
- Check CORS configuration in backend/api.py
- Look for red dot next to "API Status" in dashboard topbar
- Check browser console (F12) for CORS errors

**Cloud Run deployment fails**
- Ensure Dockerfile is correct
- Check requirements.txt has all dependencies
- Verify billing is enabled

**Out of memory**
- Increase Cloud Run memory: `--memory 2Gi`
- Reduce dataset size in data_generator.py
