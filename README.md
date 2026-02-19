# 🏥 Hospital Data Insights Pipeline

A sophisticated, production-ready healthcare analytics platform featuring multi-page interactive dashboards, AI-powered clinical decision support, synthetic data generation, ETL processing, DuckDB data warehouse, and machine learning predictions.

## 📋 Table of Contents

- [Features](#features)
- [Dashboard Previews](#dashboard-previews)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Dashboard Features](#dashboard-features)
- [Machine Learning](#machine-learning)

## ✨ Features

### Data Pipeline
- ✅ **Enhanced Synthetic Data Generation**: Realistic hospital datasets with 5,000 patients, 15,000+ visits
- ✅ **Advanced ETL Processing**: Data cleaning, transformation, and validation
- ✅ **DuckDB Warehouse**: Star schema with fact and dimension tables
- ✅ **Rich Data Fields**: Triage levels, wards, diagnosis codes, billing, temporal patterns

### Machine Learning
- 🎯 **Readmission Risk Prediction**: Random Forest classifier (97.9% accuracy)
- ⏱️ **Wait Time Forecasting**: Predict department wait times by hour/day
- 📊 **Model Evaluation**: Comprehensive metrics (ROC-AUC, RMSE, precision/recall)
- 🤖 **AI Clinical Recommendations**: Evidence-based interventions by risk level

### Multi-Page Analytics Dashboard
- 📊 **Overview Dashboard**: 6 KPI cards, monthly trends, department distribution
- 🏥 **OPD Analytics**: Wait times by department/hour/day, visit volume patterns
- 🛏️ **Inpatient Analytics**: Ward LOS, readmissions by diagnosis, monthly trends
- 🤖 **AI Risk Assessment**: Interactive patient risk scoring with clinical recommendations
- 🎨 **Professional UI**: Gradient cards, responsive design, collapsible filters
- 📈 **12+ Interactive Charts**: Line, bar, doughnut charts with legends
- 💾 **CSV Export**: Population-level risk stratification export
- 🔍 **Smart Filtering**: Department selection, risk level filters, sortable tables

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

## 🏗️ Architecture

```
Frontend (Vanilla JS + Chart.js)
            ↓
    FastAPI REST API
            ↓
    Analytics Engine & ML Models
    (TabPFN, Random Forest, Ridge)
            ↓
    DuckDB Data Warehouse
    (Star Schema)
```

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI**: Modern REST API framework
- **DuckDB**: Embedded analytical database
- **Pandas**: Data manipulation
- **Scikit-learn**: Traditional ML models
- **TabPFN**: Large Tabular Foundation Model (primary classifier)
- **Uvicorn**: ASGI server

### Frontend
- **HTML5/CSS3/JavaScript**: Vanilla implementation
- **Chart.js**: Data visualization
- **Responsive Design**: Mobile-friendly

### Data
- **Parquet**: Efficient data storage
- **DuckDB**: SQL analytics
- **Faker**: Synthetic data generation

## 📁 Project Structure

```
hospital-insights/
│
├── backend/
│   ├── api.py                      # FastAPI application with 14 endpoints
│   │
│   ├── analytics/
│   │   ├── data_generator.py       # Enhanced synthetic data (triage, wards, billing)
│   │   ├── data_loader.py          # Data loading utilities
│   │   ├── etl.py                  # ETL transformations
│   │   ├── features.py             # Feature engineering
│   │   ├── models.py               # ML model training (Random Forest)
│   │   ├── predict.py              # Prediction service
│   │   └── evaluation.py           # Model evaluation & metrics
│   │
│   ├── warehouse/
│   │   └── build_db.py             # DuckDB warehouse builder (star schema)
│   │
│   ├── models/                     # Trained models (generated)
│   │   ├── classifier.pkl          # Random Forest classifier
│   │   ├── regressor.pkl           # Wait time regressor
│   │   ├── scaler_*.pkl            # Feature scalers
│   │   └── metrics.json            # Model performance
│   │
│   ├── data/
│   │   ├── raw/                    # Raw parquet files (generated)
│   │   │   ├── patients.parquet
│   │   │   ├── visits.parquet
│   │   │   └── admissions.parquet
│   │   ├── processed/              # Cleaned parquet files (generated)
│   │   └── hospital_warehouse.db   # DuckDB database
│   │
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── index.html                  # Multi-page dashboard (4 pages)
│   ├── dashboard.js                # Dashboard logic (800+ lines, 20+ functions)
│   └── styles.css                  # Professional styling (900+ lines)
│
├── scripts/
│   └── run_pipeline.py             # Complete pipeline runner
│
├── README.md                       # This file
├── QUICKSTART.md                   # Quick start guide
└── ENHANCED_DASHBOARD_GUIDE.md     # Detailed dashboard documentation
```

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python -c "import fastapi, duckdb, pandas, sklearn; print('✅ Dependencies installed')"
```

### Optional: TabPFN Installation

TabPFN is optional. The system gracefully falls back to Random Forest if unavailable.

```bash
pip install tabpfn
```

## 🚀 Quick Start

### Run the Complete Pipeline (3 Commands)

```bash
# 1. Generate data, build warehouse, train models
python scripts/run_pipeline.py

# 2. Start API server
cd backend
uvicorn api:app --reload

# 3. Open frontend (in a new terminal / browser)
# Simply open frontend/index.html in your browser
# Or use Python's built-in server:
cd frontend
python -m http.server 8080
# Then visit: http://localhost:8080
```

## 📖 Usage Guide

### 1. Generate Data & Train Models

```bash
python scripts/run_pipeline.py
```

This will:
- Generate 5,000 synthetic patients
- Create 15,000 hospital visits
- Build ETL pipeline
- Create DuckDB warehouse with star schema
- Engineer ML features
- Train classification model (TabPFN or Random Forest)
- Train regression model (Wait time prediction)
- Save all models and metrics

**Expected Duration**: 2-5 minutes

### 2. Start the API Server

```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Open the Dashboard

Simply open `frontend/index.html` in your web browser.

Or serve it locally:
```bash
cd frontend
python -m http.server 8080
```

Then visit: http://localhost:8080

## 🔌 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health and info |
| `/health` | GET | Detailed health check |
| `/summary` | GET | Overall statistics (patients, visits, admissions) |
| `/department-stats` | GET | Department analytics |
| `/monthly-trends` | GET | Monthly visit trends |
| `/opd-analytics` | GET | OPD wait times by dept/hour/day |
| `/inpatient-analytics` | GET | Ward LOS, readmissions, trends |
| `/patients/list?limit=1000` | GET | Patient list with profiles |
| `/billing-summary` | GET | Revenue and billing stats |
| `/risk/{patient_id}` | GET | Patient risk assessment |
| `/predict-risk` | POST | Custom risk prediction |
| `/wait-time-forecast` | GET | Wait time forecast |
| `/metrics` | GET | Model performance metrics |
| `/patients/high-risk` | GET | High-risk patient list |

### Example API Calls

#### Get Summary Statistics
```bash
curl http://localhost:8000/summary
```

#### Get OPD Analytics
```bash
curl http://localhost:8000/opd-analytics
```

#### Check Patient Risk
```bash
curl http://localhost:8000/risk/P00001
```

#### Forecast Wait Time
```bash
curl "http://localhost:8000/wait-time-forecast?department=Emergency&hour=10&day_of_week=0"
```

#### Predict Custom Risk
```bash
curl -X POST http://localhost:8000/predict-risk \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "bmi": 32.5,
    "chronic_condition_count": 2,
    "total_visits": 8,
    "total_admissions": 3,
    "is_smoker": 1,
    "senior_citizen": 1
  }'
```

## 📱 Dashboard Features

### Multi-Page Navigation
The dashboard includes 4 specialized pages accessible via tab navigation:

#### 📊 Overview Dashboard
- **6 Gradient KPI Cards**: Total Patients, Visits, Admissions, Avg Wait Time, Readmission Rate, Revenue
- **Monthly Visit Trends**: Line chart showing 12-month trend
- **Department Distribution**: Doughnut chart with department breakdown
- **Real-time Status**: API health indicator and last update timestamp

#### 🏥 OPD Analytics
- **Wait Time by Department**: Horizontal bar chart ranking departments
- **Hourly Patterns**: Line chart showing wait times across 24 hours
- **Daily Visit Volume**: Bar chart showing patterns by day of week
- **Department Volume**: Doughnut chart showing visit distribution

#### 🛏️ Inpatient & Ward Analytics
- **Average LOS by Ward**: Bar chart comparing 8 wards (ICU, CCU, NICU, Pediatric, Ward A-D)
- **Readmission Rates by Diagnosis**: Horizontal bar chart showing ICD-10 codes
- **Monthly Admission Trends**: Line chart showing 24-month historical trends

#### 🤖 AI-Powered Patient Risk Assessment
- **Patient Selector**: Dropdown with 1,000 patients
- **Risk Gauge**: Interactive canvas showing 0-100% risk score
- **Color-Coded Risk Levels**: 🟢 Low (<35%), 🟡 Medium (35-60%), 🔴 High (≥60%)
- **Clinical Profile**: Age, gender, BMI, smoking, chronic conditions, visit history
- **Evidence-Based Recommendations**: 
  - High Risk: 24-hour interventions (discharge planning, home health referral)
  - Medium Risk: Enhanced monitoring protocols
  - Low Risk: Standard discharge procedures
- **Risk Factors Analysis**: Impact scoring (e.g., Diabetes +18%, Hypertension +12%)
- **Population Table**: 1,000 patients with sorting and filtering
- **CSV Export**: Download high-risk patient list

### Smart Features
- ✅ **Collapsible Department Filter**: Select/deselect departments with checkbox controls
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Real-time Updates**: Auto-refresh every 5 minutes
- ✅ **Professional Styling**: Medical-themed gradients, hover effects, smooth animations

## 🤖 Machine Learning

### Readmission Risk Classification

**Primary Model**: Random Forest Classifier
- High accuracy (97.9% on test set)
- Robust to overfitting with ensemble approach
- Feature importance for clinical insights

**Features Used**:
- Age, BMI, smoking status
- Chronic condition count (diabetes, hypertension, heart disease)
- Visit history (total visits, admissions)
- Admission patterns
- Length of stay metrics

**Metrics**:
- **Accuracy**: 97.9%
- ROC-AUC, Precision, Recall, F1-Score
- Feature importance ranking
- Confusion matrix analysis

### Wait Time Prediction

**Model**: Random Forest Regressor

**Features**:
- Hour of day (0-23)
- Day of week (0-6)
- Department type
- Weekend flag
- Emergency department flag
- Triage level

**Metrics**:
- RMSE (Root Mean Squared Error): ~19.38 minutes
- MAE (Mean Absolute Error)
- R² Score

### Clinical Decision Support

The AI system provides risk-stratified recommendations:

**High Risk (≥60%)**:
- Schedule discharge planning meeting within 24 hours
- Arrange follow-up within 3 days post-discharge
- Evaluate for home health services
- Implement daily monitoring protocol

**Medium Risk (35-60%)**:
- Schedule follow-up within 7 days
- Complete medication reconciliation
- Bi-weekly check-ins for first month
- Consider care coordinator assignment

**Low Risk (<35%)**:
- Standard discharge procedures
- Routine follow-up within 14-30 days
- Standard education materials

## 📊 Data Warehouse Schema

### Star Schema Design

**Fact Table**: `fact_visits`
- visit_id, patient_id, date_id, department_id
- wait_time_minutes, is_admitted, length_of_stay_days
- satisfaction_score, readmitted_30d_flag

**Dimension Tables**:
- `dim_patient`: Patient demographics
- `dim_department`: Department information
- `dim_date`: Date dimensions (year, month, quarter, day_of_week)

### Sample Queries

Access DuckDB directly:
```python
import duckdb
conn = duckdb.connect('backend/data/hospital_warehouse.db')

# Department statistics
conn.execute("""
    SELECT dd.department_name, COUNT(*) as visits
    FROM fact_visits fv
    JOIN dim_department dd ON fv.department_id = dd.department_id
    GROUP BY dd.department_name
""").df()
```

## 🌐 Deployment

### Firebase Hosting (Frontend)

```bash
cd frontend
firebase login
firebase init hosting
firebase deploy
```

### Google Cloud Run (Backend)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
```

Deploy:
```bash
gcloud run deploy hospital-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
DB_PATH=backend/data/hospital_warehouse.db

# Models
MODEL_DIR=backend/models
```

### Customization

**Change dataset size**:
Edit `scripts/run_pipeline.py`:
```python
generator = HospitalDataGenerator(n_patients=10000, n_visits=30000)
```

**Change API URL** (frontend):
Edit `frontend/dashboard.js`:
```javascript
const API_BASE_URL = 'https://your-api-url.com';
```

## 📈 Performance

| Metric | Value |
|--------|-------|
| Data Generation | ~30 seconds for 5K patients |
| ETL Processing | ~10 seconds |
| Warehouse Build | ~15 seconds |
| Model Training | ~60 seconds (TabPFN/RF) |
| API Response Time | <100ms (cached queries) |

## 🧪 Testing

### Test Data Generation
```bash
python backend/analytics/data_generator.py
```

### Test ETL Pipeline
```bash
python backend/analytics/etl.py
```

### Test ML Models
```bash
python backend/analytics/models.py
```

### Test API
```bash
pytest backend/tests/  # If tests are added
```

## 🐛 Troubleshooting

### TabPFN Not Available
- System automatically falls back to Random Forest
- Check: `pip list | grep tabpfn`
- Install: `pip install tabpfn`

### API Connection Failed
- Ensure API is running: `http://localhost:8000/health`
- Check CORS settings in `backend/api.py`
- Verify frontend API_BASE_URL

### Database Not Found
- Run pipeline first: `python scripts/run_pipeline.py`
- Check file exists: `backend/data/hospital_warehouse.db`

### Memory Issues
- Reduce dataset size in `run_pipeline.py`
- TabPFN has dataset size limits (~1000 samples)

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, please open an issue on GitHub.

## 🎓 Educational Use

This project demonstrates:
- Modern data pipeline architecture
- ETL best practices
- Data warehouse design (star schema)
- Machine learning deployment
- REST API development
- Interactive dashboard creation
- Production-ready project structure

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **DuckDB** for the embedded analytics database
- **TabPFN** for the foundation model
- **Chart.js** for beautiful visualizations

---

**Built with ❤️ for Healthcare Analytics**

*Last Updated: February 2026*
