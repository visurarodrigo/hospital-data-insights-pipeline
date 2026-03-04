# 🏥 Hospital Data Insights Pipeline

A production-ready healthcare analytics platform featuring **Large Tabular Model (LTM)** for AI-powered clinical decision support, interactive dashboards, ETL pipeline, DuckDB data warehouse, and state-of-the-art machine learning risk predictions.

**Live Demo (Frontend)**: https://hospital-insights-c9c40.web.app  
**Source Code**: https://github.com/visurarodrigo/hospital-data-insights-pipeline

*Note: Backend runs locally - see [Quick Start](#-quick-start) for setup*

---

## 📋 Table of Contents

- [Features](#-features)
- [Dashboard Previews](#-dashboard-previews)
- [Quick Start](#-quick-start)
- [Architecture](#️-architecture)
- [API Documentation](#-api-documentation)
- [Machine Learning](#-machine-learning)
- [Deployment](#-deployment)

---

## ✨ Features

**Data Engineering**
- 🔄 Synthetic data generation (5,000 patients, 15,000+ visits)
- 🛠️ ETL pipeline with data validation and cleaning
- 🗄️ DuckDB data warehouse (star schema)
- 📊 Real-time analytics with SQL queries

**Machine Learning - Large Tabular Model (LTM)**
- 🔬 State-of-the-art Large Tabular Foundation Model integration
- 🎯 Readmission risk prediction with foundation model (97.9% accuracy)
- ⏱️ Wait time forecasting by department/hour
- 🤖 AI-powered clinical recommendations
- 🔄 Intelligent hybrid ML approach (LTM + Traditional ML)
- 📈 Comprehensive model evaluation metrics

**Interactive Dashboard**
- 📊 4-page multi-view analytics (Overview, OPD, Inpatient, AI Risk)
- 📈 12+ interactive visualizations (Chart.js)
- 🎨 Professional UI with gradient cards
- 💾 CSV export for risk stratification
- 🔍 Smart filters and real-time updates

## 📸 Dashboard Previews

### Overview Dashboard
![Overview Dashboard](frontend/Screenshots/Overview%20Page.png)
*6 KPI cards showing patients, visits, admissions, wait time, readmission rate, and revenue with monthly trends and department distribution charts*

### OPD Analytics
![OPD Analytics](frontend/Screenshots/OPD%20Page.png)
*Outpatient department analytics with wait time analysis by department, hour of day, and day of week patterns*

### Inpatient & Ward Analytics
![Inpatient Analytics](frontend/Screenshots/inpatient%20page.png)
*Ward-level analysis showing average length of stay, readmission rates by diagnosis, and monthly admission trends*

### AI-Powered Patient Risk Assessment
![Risk Assessment](frontend/Screenshots/risk%20page.png)
*Interactive patient risk scoring with clinical recommendations, risk factor analysis, and population-level risk stratification with CSV export*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│   Frontend (HTML/CSS/JS + Chart.js)        │
│   - Overview, OPD, Inpatient, AI Risk      │
└───────────────────┬─────────────────────────┘
                    │ REST API
┌───────────────────▼─────────────────────────┐
│   FastAPI Backend (14 Endpoints)           │
│   - Analytics Engine                        │
│   - ML Prediction Service                   │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│   ML Models (Hybrid LTM Approach)          │
│   - LTM Classifier (97.9% accuracy)         │
│   - Regressor (Wait Time forecasting)       │
└─────────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│   DuckDB Data Warehouse (Star Schema)      │
│   - fact_visits, dim_patient, dim_dept     │
└─────────────────────────────────────────────┘
```

**Tech Stack**
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pandas, Scikit-learn
- **Database**: DuckDB (SQL analytics), Parquet (storage)
- **Frontend**: Vanilla JavaScript, Chart.js, HTML5/CSS3
- **ML**: TabPFN (Large Tabular Foundation Model - Primary), Random Forest (Fallback), Feature Engineering

---

## 🚀 Quick Start

### Installation

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt
```

### Running Locally

```bash
# 1. Generate data & train models (~30 seconds)
python scripts/run_pipeline.py

# 2. Start API server
python -m uvicorn backend.api:app --reload --port 8000

# 3. Open frontend
# Option A: Double-click frontend/index.html
# Option B: Serve with Python
cd frontend
python -m http.server 8080
# Visit: http://localhost:8080
```

**Access Points:**
- 🌐 Dashboard: http://localhost:8080
- 📡 API Docs: http://localhost:8000/docs
- ✅ Health Check: http://localhost:8000/health

---

## 🔌 API Documentation

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with system status |
| `/summary` | GET | Overall KPI statistics |
| `/opd-analytics` | GET | OPD wait times & patterns |
| `/inpatient-analytics` | GET | Ward LOS & readmissions |
| `/patients/list` | GET | Patient list (query: `?limit=1000`) |
| `/risk/{patient_id}` | GET | Individual risk assessment |
| `/predict-risk` | POST | Custom risk prediction |
| `/wait-time-forecast` | GET | Department wait time forecast |
| `/metrics` | GET | ML model performance |

**Interactive API Docs**: http://localhost:8000/docs

### Example Usage

```bash
# Get statistics
curl http://localhost:8000/summary

# Patient risk assessment
curl http://localhost:8000/risk/P00001

# Wait time forecast
curl "http://localhost:8000/wait-time-forecast?department=Emergency&hour=14&day_of_week=1"

# Predict custom risk
curl -X POST http://localhost:8000/predict-risk \
  -H "Content-Type: application/json" \
  -d '{"age": 65, "bmi": 32.5, "chronic_condition_count": 2, "total_visits": 8}'
```

---

## 🤖 Machine Learning - Large Tabular Model (LTM)

### 🎯 Primary Innovation: Large Tabular Foundation Model

This project leverages a **Large Tabular Model (LTM)** - a state-of-the-art foundation model that uses in-context learning for tabular data, similar to how GPT works for language tasks.

**Why LTM is Revolutionary:**
- 🧠 **Foundation Model**: Pre-trained on millions of synthetic tabular datasets
- ⚡ **Zero Hyperparameter Tuning**: No manual configuration needed
- 🎯 **In-Context Learning**: Learns from your data without traditional training
- 🏆 **Superior Performance**: Often outperforms tuned Random Forests and Gradient Boosting
- 🔬 **Cutting-Edge Research**: Based on Transformer architecture for tabular data

### Readmission Risk Prediction

**Approach**: Hybrid LTM Architecture  
**Dataset**: 5,000 patients with 15,000+ clinical visits

**Intelligent Model Selection:**
```
   LTM (Primary) → If dataset exceeds limit → Traditional ML (Fallback)
        ↓                                              ↓
  In-context learning                        Ensemble classifier
  (Foundation Model)                         (Classical ML)
```

**Model Performance:**
- **Accuracy**: 97.9%
- **Precision**: 97.9%
- **Recall**: 100%
- **ROC-AUC**: 97.87%
- **Features**: Age, BMI, chronic conditions, visit history, smoking status, previous admissions
- **Output**: Risk score (0-100%), risk level, personalized clinical recommendations

**LTM Implementation:**
- Intelligent fallback mechanism for large datasets
- Maintains high accuracy across all dataset sizes
- Zero-configuration foundation model approach

**Risk Stratification**:
- 🔴 **High (≥60%)**: Discharge planning within 24h, follow-up in 3 days
- 🟡 **Medium (35-60%)**: Follow-up in 7 days, medication reconciliation
- 🟢 **Low (<35%)**: Standard discharge, routine follow-up

### Wait Time Forecasting

**Model**: Random Forest Regressor
- **RMSE**: ~19.3 minutes
- **Features**: Hour of day, day of week, department, triage level, historical patterns
- **Use Case**: Predict wait times by department/hour for resource planning

### Model Performance

```python
Classification Metrics (Readmission):
  Accuracy:  97.9%
  Precision: 97.9%
  Recall:    100%
  ROC-AUC:   97.87%

Regression Metrics (Wait Time):
  RMSE: 19.29 minutes
  MAE:  15.27 minutes
  R²:   0.1833
```

Access metrics via API: `GET /metrics`

### 🔬 LTM vs Traditional ML

| Feature | LTM (Foundation Model) | Traditional ML (Fallback) |
|---------|------------------------|----------------------------|
| **Type** | Foundation Model | Ensemble Classifier |
| **Training** | Pre-trained (zero-shot) | Task-specific training |
| **Hyperparameters** | None needed | Manual tuning required |
| **Approach** | In-context learning | Statistical modeling |
| **Innovation Level** | 🔬 Cutting-edge research | ✅ Industry standard |

**Our Hybrid LTM Approach:**  
The system intelligently leverages Large Tabular Model for foundation model capabilities and automatically falls back to traditional ML for large-scale production datasets, ensuring **both innovation and scalability**.

---

## 🌐 Deployment

### Frontend (Firebase Hosting) ✅ Deployed

```bash
# Deploy frontend
firebase login
firebase deploy --only hosting
```

**Live URL**: https://hospital-insights-c9c40.web.app

### Backend (Local Development) 🖥️

**Current Setup**: Backend runs locally for development and testing

```bash
# Run backend locally
python -m uvicorn backend.api:app --reload --port 8000
```

**Access**: http://localhost:8000

### Backend Cloud Deployment (Optional - Not Yet Implemented)

If you want to deploy the backend to production, here are the options:

**Option 1: Railway**
1. Visit https://railway.app
2. Connect GitHub repository
3. Deploy automatically
4. Update `frontend/dashboard.js` with Railway URL

**Option 2: Google Cloud Run**
```bash
gcloud run deploy hospital-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

**Note**: After backend deployment, update API URL in `frontend/dashboard.js`:
```javascript
const API_BASE_URL = 'https://your-deployed-api-url.com';
```

---

## 📊 Project Structure

```
hospital-insights/
├── backend/
│   ├── api.py                    # FastAPI app (14 endpoints)
│   ├── analytics/
│   │   ├── data_generator.py     # Synthetic data generation
│   │   ├── etl.py                # ETL pipeline
│   │   ├── models.py             # ML training
│   │   ├── predict.py            # Prediction service
│   │   └── evaluation.py         # Model evaluation
│   ├── warehouse/
│   │   └── build_db.py           # DuckDB warehouse
│   ├── data/                     # Generated data
│   └── models/                   # Trained models
├── frontend/
│   ├── index.html                # Multi-page dashboard
│   ├── dashboard.js              # Dashboard logic
│   └── styles.css                # Styling
└── scripts/
    └── run_pipeline.py           # Pipeline runner
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **API offline** | Run `python -m uvicorn backend.api:app --reload` |
| **No data found** | Run `python scripts/run_pipeline.py` first |
| **Model training errors** | Ensure scikit-learn is installed: `pip install scikit-learn` |
| **CORS error** | Check `API_BASE_URL` in `frontend/dashboard.js` |
| **Port in use** | Change port: `--port 8001` |

---

## 📚 Additional Resources

- **Quick Start Guide**: See [QUICKSTART.md](QUICKSTART.md)
- **Dashboard Guide**: See [ENHANCED_DASHBOARD_GUIDE.md](ENHANCED_DASHBOARD_GUIDE.md)
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Interactive API Docs**: http://localhost:8000/docs

---

## 🎓 Key Learnings

This project demonstrates:
- ✅ End-to-end data pipeline architecture
- ✅ ETL best practices with validation
- ✅ Star schema data warehouse design
- 🔬 **Large Tabular Model (LTM) integration**
- ✅ Hybrid LTM approach (Foundation Model + Traditional ML)
- ✅ RESTful API development
- ✅ Interactive data visualization
- ✅ Healthcare analytics & clinical decision support

---

## 📝 License

Educational and demonstration purposes.

---

## 🤝 Contributing

Contributions welcome! Please fork the repository and submit a pull request.

---

**Built with ❤️ for Healthcare Analytics**

*Repository*: https://github.com/visurarodrigo/hospital-data-insights-pipeline  
*Last Updated*: March 2026