# 🚀 Hospital Insights Pipeline - Quick Start Guide

> **📍 Setup Type**: Local Development  
> **Frontend**: Also available at https://hospital-insights-c9c40.web.app  
> **Backend**: Runs locally (API server on your machine)

## ⚡ 3-Step Launch

### Step 1: Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### Step 2: Run Pipeline
```powershell
python scripts/run_pipeline.py
```

### Step 3: Start API Server
```powershell
python -m uvicorn backend.api:app --reload --port 3000
```

Then open `frontend/index.html` in your browser!

**Pro Tip**: Try the dark mode toggle in the top-right corner! 🌓

## 📊 What Gets Created

After running the pipeline:

✅ **Data Files**:
- `backend/data/raw/` - Synthetic hospital data (5,000 patients, 15,000+ visits)
- `backend/data/processed/` - Cleaned data with enhanced fields (triage, wards, billing)
- `backend/data/hospital_warehouse.db` - DuckDB analytics database (star schema)

✅ **ML Models**:
- `backend/models/classifier.pkl` - LTM hybrid readmission risk model (97.9% accuracy)
- `backend/models/regressor.pkl` - Wait time prediction model (RMSE ~19.38 min)
- `backend/models/scaler_*.pkl` - Feature scalers
- `backend/models/metrics.json` - Model performance metrics

## 🔍 Quick Tests

### Test API
```powershell
# Check health
Invoke-WebRequest "http://localhost:3000/health" -UseBasicParsing

# Get summary
Invoke-WebRequest "http://localhost:3000/summary" -UseBasicParsing

# Get OPD analytics
Invoke-WebRequest "http://localhost:3000/opd-analytics" -UseBasicParsing

# Check patient risk
Invoke-WebRequest "http://localhost:3000/risk/P00001" -UseBasicParsing
```

### Test Dashboard
Open `frontend/index.html` in your browser

You should see:
- ✅ Modern SaaS-style interface with clean design
- ✅ Dark/light mode toggle in top-right corner
- ✅ 6 interactive KPI cards with gradient backgrounds
- ✅ Real-time API status indicator (green dot = healthy)
- ✅ 4-page navigation (Overview, OPD Analytics, Inpatient & Ward, AI Risk Assessment)
- ✅ 12+ interactive charts with modern color palette
- ✅ Toast notifications for user feedback
- ✅ Smart department filter with chip-style selection
- ✅ Loading states with skeleton loaders
- ✅ Fully responsive design (works on mobile)
- ✅ AI patient risk assessment with clinical recommendations
- ✅ Population-level risk stratification with CSV export

## 🐛 Common Issues

### 1. "ModuleNotFoundError: No module named 'fastapi'"
```powershell
cd backend
pip install -r requirements.txt
```

### 2. "Database not found"
```powershell
python scripts/run_pipeline.py
```

### 3. "API connection failed" (in frontend)
- Ensure API is running: http://localhost:3000/health
- Start API with: `python -m uvicorn backend.api:app --reload --port 3000`
- Check browser console for errors (F12)
- Dashboard shows "API Offline" (red dot) if server isn't running
- Frontend expects API on port 3000 (configured in dashboard.js)

### 4. Charts not displaying
- Hard refresh browser (Ctrl+F5 or Ctrl+Shift+R)
- Check browser console for JavaScript errors
- Verify API endpoints returning data

### 5. Multiple servers running (Port 3000 in use)
```powershell
# Kill all Python processes
Get-Process python* | Stop-Process -Force

# Restart server
python -m uvicorn backend.api:app --reload --port 3000
```

### 6. Dark mode not saving
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for localStorage errors
- Theme preference is saved in browser localStorage

### 7. Toast notifications not appearing
- Hard refresh browser (Ctrl+F5)
- Check browser console for JavaScript errors
- Ensure dashboard.js is loaded correctly

## 📈 Expected Performance

| Task | Time |
|------|------|
| Data Generation | ~10s |
| ETL + Warehouse | ~15s |
| Model Training | ~5s |
| **Total Pipeline** | **~30s** |

## 🎯 Key Features to Try

### Overview Dashboard (Page 1)
1. View 6 KPI cards with real-time stats
2. Explore monthly visit trends (12-month chart)
3. Analyze department distribution

### OPD Analytics (Page 2)
1. Compare wait times across departments
2. Identify peak hours (9 AM - 5 PM typically highest)
3. Analyze daily visit patterns (weekday vs weekend)
4. View department-wise visit volume

### Inpatient Analytics (Page 3)
1. Compare average length of stay by ward
2. Identify high-risk diagnoses for readmission
3. Track monthly admission trends over 24 months

### AI Risk Assessment (Page 4)
1. **Individual Assessment**: 
   - Select patient from dropdown (1,000 patients available)
   - Click "Assess Risk" to see risk score (0-100%)
   - View clinical profile and risk factors
   - Read evidence-based recommendations
2. **Population View**:
   - Filter by risk level (All/High/Medium/Low)
   - Sort by risk score or age
   - Adjust display limit (20/50/100/200)
   - Export high-risk patients to CSV

## 📁 Project Stats

- **Patients**: 5,000
- **Visits**: 15,000+
- **Departments**: 10 (Cardiology, Orthopedics, Neurology, Pediatrics, Emergency, etc.)
- **Wards**: 8 (Ward A/B/C/D, ICU, CCU, NICU, Pediatric Ward)
- **Diagnosis Codes**: 10 ICD-10 codes
- **API Endpoints**: 14
- **Dashboard Pages**: 4
- **Interactive Charts**: 12+
- **Lines of Code**: ~3,500+

## 🌐 API Documentation

Full interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick API Reference

| Endpoint | Description |
|----------|-------------|
| `/health` | Service health check |
| `/summary` | Overall statistics |
| `/opd-analytics` | OPD wait times & patterns |
| `/inpatient-analytics` | Ward LOS & readmissions |
| `/patients/list?limit=1000` | Patient profiles |
| `/billing-summary` | Revenue stats |
| `/risk/{patient_id}` | Individual risk score |

## 💡 Pro Tips

1. **Check API first**: Always verify API is running at http://localhost:8000/health
2. **Use correct path**: Start API with `python -m uvicorn backend.api:app --reload --port 8000`
3. **Browser refresh**: Hard refresh (Ctrl+F5) if dashboard doesn't update
4. **Charts not loading**: Check browser Console (F12) for API connection errors
5. **Data exploration**: Use DuckDB CLI to query warehouse directly
6. **Customization**: Edit dataset size in `data_generator.py`
7. **Risk assessment**: Try high-risk patients (age >65, multiple conditions)
8. **CSV export**: Download population risk data for offline analysis

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **DuckDB**: https://duckdb.org
- **Chart.js**: https://www.chartjs.org
- **Random Forest**: https://scikit-learn.org/stable/modules/ensemble.html

## ✨ Next Steps

1. ✅ Run the pipeline
2. ✅ Start API server
3. ✅ Explore 4 dashboard pages
4. 📊 Test AI risk assessment
5. 📈 Export population risk data
6. 🔧 Customize data generation
7. 🚀 Deploy to production (optional)

## 🔄 Regenerate Data

To create fresh data:
```powershell
python scripts/run_pipeline.py
```

This will:
- Regenerate 5,000 patients and 15,000+ visits
- Rebuild warehouse with new data
- Retrain ML models with updated metrics
- Preserve model performance (~97.9% accuracy)

---

**Need detailed help?** 
- Check **README.md** for full documentation
- Check **ENHANCED_DASHBOARD_GUIDE.md** for dashboard features
- Visit http://localhost:8000/docs for API reference
