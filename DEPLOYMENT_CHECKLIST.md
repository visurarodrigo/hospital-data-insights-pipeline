# 🚀 Quick Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Pipeline has been run (`python scripts/run_all.py`)
- [ ] Data files exist in `data/processed/`
- [ ] Models exist in `models/`
- [ ] Database exists at `warehouse/hospital.duckdb`
- [ ] Dashboard runs locally (`streamlit run dashboard/app.py`)
- [ ] GitHub repository created
- [ ] All changes committed to Git

## 📝 Streamlit Cloud Deployment (5 Minutes)

### Step 1: Prepare Project (2 min)
```bash
# Run automated preparation
python scripts/prepare_deployment.py

# Or manually:
python scripts/run_all.py
```

### Step 2: Commit to GitHub (1 min)
```bash
git add .
git add -f data/processed/*.csv
git add -f models/*.joblib models/*.json
git add -f warehouse/hospital.duckdb
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### Step 3: Deploy on Streamlit Cloud (2 min)
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `dashboard/app.py`
6. Click "Deploy!"

**Your app will be live at:** `https://[your-app-name].streamlit.app`

## 🐳 Docker Deployment (Alternative)

### Build & Run Locally
```bash
docker build -t hospital-insights .
docker run -p 8501:8501 hospital-insights
# Access at http://localhost:8501
```

### Deploy to Cloud Platforms

**Render.com:**
```bash
# Push to GitHub, then:
# 1. Create Web Service on Render
# 2. Connect GitHub repo
# 3. Set Docker build
# 4. Deploy!
```

**Railway:**
```bash
railway login
railway init
railway up
# Auto-detects Dockerfile
```

**Google Cloud Run:**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/hospital-insights
gcloud run deploy --image gcr.io/PROJECT-ID/hospital-insights --platform managed
```

## 🔧 Troubleshooting

### ❌ "FileNotFoundError: data/processed/..."
**Fix:** Ensure you've run the pipeline and committed data files:
```bash
python scripts/run_all.py
git add -f data/processed/*.csv
git commit -m "Add processed data"
git push
```

### ❌ "ModuleNotFoundError: No module named 'xxx'"
**Fix:** Check requirements.txt is complete:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### ❌ "File size too large (>100MB)"
**Fix:** Use Git LFS or reduce data size:
```bash
# Option 1: Git LFS
git lfs install
git lfs track "*.duckdb"
git add .gitattributes warehouse/hospital.duckdb
git commit -m "Add LFS"
git push

# Option 2: Reduce data in config.yaml
# Change num_patients: 5200 → 1000
```

### ❌ App crashes on startup
**Fix:** Check Streamlit Cloud logs:
1. Go to app dashboard
2. Click "Manage app" → "Logs"
3. Review error messages

## 📊 File Size Reference

Typical deployment package:
- Database: ~5-50 MB (depends on num_patients)
- Models: ~1-5 MB
- Processed Data: ~2-20 MB
- **Total:** ~10-75 MB (within limits ✅)

If over 100MB:
- Reduce `num_patients` in config.yaml
- Use Git LFS for database
- Compress with DuckDB vacuum

## 🎯 Success Indicators

After deployment, verify:
- ✅ Dashboard loads without errors
- ✅ All 6 navigation pages work
- ✅ Charts and visualizations render
- ✅ Department filters function
- ✅ AI predictions work
- ✅ CSV exports download

## 📚 Additional Resources

- **Full Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Streamlit Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **Docker Docs:** https://docs.docker.com/
- **Git LFS:** https://git-lfs.github.com/

---

**Estimated Total Time:** 5-10 minutes for Streamlit Cloud deployment 🚀
