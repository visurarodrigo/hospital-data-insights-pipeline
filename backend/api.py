"""
FastAPI Backend for Hospital Data Insights
Exposes analytics and ML predictions via REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import pandas as pd
import duckdb
import os
from datetime import datetime

# Import analytics modules
from backend.analytics.predict import PredictionService
from backend.analytics.evaluation import ModelEvaluator

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Data Insights API",
    description="Analytics and ML predictions for healthcare data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
prediction_service = None
db_connection = None
evaluator = None


# Pydantic models for request/response
class PatientRiskRequest(BaseModel):
    """Request model for patient risk prediction"""
    patient_id: Optional[str] = None
    age: float
    bmi: float
    chronic_condition_count: int = 0
    total_visits: int = 1
    total_admissions: int = 0
    avg_wait_time: float = 30.0
    visit_frequency: float = 0.0
    admission_rate: float = 0.0
    is_smoker: int = 0
    has_chronic_condition: int = 0
    high_bmi: int = 0
    senior_citizen: int = 0
    multiple_conditions: int = 0
    frequent_visitor: int = 0


class WaitTimeRequest(BaseModel):
    """Request model for wait time prediction"""
    hour: int = 10
    day_of_week: int = 0
    is_weekend: int = 0
    is_emergency: int = 0
    department_features: Optional[Dict[str, int]] = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global prediction_service, db_connection, evaluator
    
    print("\n" + "="*60)
    print("🚀 STARTING HOSPITAL INSIGHTS API")
    print("="*60 + "\n")
    
    # Initialize prediction service
    try:
        prediction_service = PredictionService(model_dir='backend/models')
        print("✅ Prediction service initialized")
    except Exception as e:
        print(f"⚠️  Could not initialize prediction service: {e}")
        prediction_service = None
    
    # Initialize DuckDB connection
    try:
        db_path = 'backend/data/hospital_warehouse.db'
        if os.path.exists(db_path):
            db_connection = duckdb.connect(db_path, read_only=True)
            print("✅ Database connection established")
        else:
            print(f"⚠️  Database not found at {db_path}")
            db_connection = None
    except Exception as e:
        print(f"⚠️  Could not connect to database: {e}")
        db_connection = None
    
    # Initialize evaluator
    try:
        evaluator = ModelEvaluator(model_dir='backend/models')
        print("✅ Model evaluator initialized")
    except Exception as e:
        print(f"⚠️  Could not initialize evaluator: {e}")
        evaluator = None
    
    print("\n✅ API Ready!\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global db_connection
    if db_connection:
        db_connection.close()
        print("✅ Database connection closed")


# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """API health check and info"""
    return {
        "status": "online",
        "service": "Hospital Data Insights API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "summary": "/summary",
            "department_stats": "/department-stats",
            "monthly_trends": "/monthly-trends",
            "patient_risk": "/risk/{patient_id}",
            "predict_risk": "/predict-risk (POST)",
            "wait_time_forecast": "/wait-time-forecast",
            "model_metrics": "/metrics",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "prediction_service": prediction_service is not None,
            "database": db_connection is not None,
            "evaluator": evaluator is not None
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/summary")
async def get_summary():
    """Get overall system summary statistics"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Total patients
        total_patients = db_connection.execute(
            "SELECT COUNT(DISTINCT patient_id) FROM dim_patient"
        ).fetchone()[0]
        
        # Total visits
        total_visits = db_connection.execute(
            "SELECT COUNT(*) FROM fact_visits"
        ).fetchone()[0]
        
        # Average wait time
        avg_wait_time = db_connection.execute(
            "SELECT AVG(wait_time_minutes) FROM fact_visits"
        ).fetchone()[0]
        
        # Total admissions
        total_admissions = db_connection.execute(
            "SELECT SUM(is_admitted) FROM fact_visits"
        ).fetchone()[0]
        
        # Admission rate
        admission_rate = (total_admissions / total_visits * 100) if total_visits > 0 else 0
        
        # Average satisfaction
        avg_satisfaction = db_connection.execute(
            "SELECT AVG(satisfaction_score) FROM fact_visits"
        ).fetchone()[0]
        
        return {
            "total_patients": int(total_patients),
            "total_visits": int(total_visits),
            "total_admissions": int(total_admissions),
            "admission_rate_percent": round(admission_rate, 2),
            "avg_wait_time_minutes": round(avg_wait_time, 1),
            "avg_satisfaction_score": round(avg_satisfaction, 2),
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")


@app.get("/department-stats")
async def get_department_stats():
    """Get statistics by department"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        query = """
            SELECT 
                dd.department_name,
                COUNT(*) as visit_count,
                AVG(fv.wait_time_minutes) as avg_wait_time,
                SUM(fv.is_admitted) as admission_count,
                AVG(fv.satisfaction_score) as avg_satisfaction
            FROM fact_visits fv
            JOIN dim_department dd ON fv.department_id = dd.department_id
            GROUP BY dd.department_name
            ORDER BY visit_count DESC
        """
        
        result = db_connection.execute(query).df()
        
        stats = []
        for _, row in result.iterrows():
            stats.append({
                "department": row['department_name'],
                "visit_count": int(row['visit_count']),
                "avg_wait_time": round(row['avg_wait_time'], 1),
                "admission_count": int(row['admission_count']),
                "avg_satisfaction": round(row['avg_satisfaction'], 2)
            })
        
        return {
            "departments": stats,
            "total_departments": len(stats),
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching department stats: {str(e)}")


@app.get("/monthly-trends")
async def get_monthly_trends(limit: int = 12):
    """Get monthly visit trends"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        query = f"""
            SELECT 
                d.year,
                d.month,
                d.month_name,
                COUNT(*) as visit_count,
                AVG(fv.wait_time_minutes) as avg_wait_time,
                AVG(fv.satisfaction_score) as avg_satisfaction
            FROM fact_visits fv
            JOIN dim_date d ON fv.date_id = d.date_id
            GROUP BY d.year, d.month, d.month_name
            ORDER BY d.year DESC, d.month DESC
            LIMIT {limit}
        """
        
        result = db_connection.execute(query).df()
        
        trends = []
        for _, row in result.iterrows():
            trends.append({
                "year": int(row['year']),
                "month": int(row['month']),
                "month_name": row['month_name'],
                "visit_count": int(row['visit_count']),
                "avg_wait_time": round(row['avg_wait_time'], 1),
                "avg_satisfaction": round(row['avg_satisfaction'], 2)
            })
        
        # Reverse to show chronological order
        trends.reverse()
        
        return {
            "trends": trends,
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")


@app.get("/risk/{patient_id}")
async def get_patient_risk(patient_id: str):
    """Get readmission risk for a specific patient"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")
    
    try:
        # Load patient data from processed features
        features_path = 'backend/data/processed/ml_features.parquet'
        if not os.path.exists(features_path):
            raise HTTPException(status_code=404, detail="Patient features not available")
        
        df_features = pd.read_parquet(features_path)
        patient_data = df_features[df_features['patient_id'] == patient_id]
        
        if len(patient_data) == 0:
            raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
        
        # Get prediction
        result = prediction_service.predict_readmission_risk(patient_data)
        
        # Add patient info
        patient_info = patient_data.iloc[0]
        result['patient_id'] = patient_id
        result['age'] = int(patient_info['age'])
        result['total_visits'] = int(patient_info.get('total_visits', 0))
        result['total_admissions'] = int(patient_info.get('total_admissions', 0))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting risk: {str(e)}")


@app.post("/predict-risk")
async def predict_risk(request: PatientRiskRequest):
    """Predict readmission risk for custom patient data"""
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")
    
    try:
        # Convert request to dict
        patient_features = request.dict(exclude={'patient_id'})
        
        # Get prediction
        result = prediction_service.predict_readmission_risk(patient_features)
        
        if request.patient_id:
            result['patient_id'] = request.patient_id
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting risk: {str(e)}")


@app.get("/wait-time-forecast")
async def get_wait_time_forecast(
    department: str = "Emergency",
    hour: int = 10,
    day_of_week: int = 0
):
    """Get predicted wait time for a department"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Get average wait time from historical data
        query = f"""
            SELECT 
                AVG(fv.wait_time_minutes) as avg_wait_time,
                MIN(fv.wait_time_minutes) as min_wait_time,
                MAX(fv.wait_time_minutes) as max_wait_time
            FROM fact_visits fv
            JOIN dim_department dd ON fv.department_id = dd.department_id
            WHERE dd.department_name = '{department}'
        """
        
        result = db_connection.execute(query).fetchone()
        
        if result is None or result[0] is None:
            # Return default if no data
            avg_wait = 30.0
            min_wait = 10.0
            max_wait = 60.0
        else:
            avg_wait, min_wait, max_wait = result
        
        # Add some variance based on time of day
        time_factor = 1.0
        if 8 <= hour <= 12:  # Morning rush
            time_factor = 1.2
        elif 17 <= hour <= 20:  # Evening rush
            time_factor = 1.3
        
        # Weekend adjustment
        weekend_factor = 0.9 if day_of_week in [5, 6] else 1.0
        
        predicted_wait = avg_wait * time_factor * weekend_factor
        
        return {
            "department": department,
            "predicted_wait_time_minutes": round(predicted_wait, 1),
            "historical_avg": round(avg_wait, 1),
            "historical_range": {
                "min": round(min_wait, 1),
                "max": round(max_wait, 1)
            },
            "factors": {
                "hour": hour,
                "day_of_week": day_of_week,
                "is_peak_time": time_factor > 1.0,
                "is_weekend": day_of_week in [5, 6]
            },
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting wait time: {str(e)}")


@app.get("/metrics")
async def get_model_metrics():
    """Get ML model performance metrics"""
    if evaluator is None:
        raise HTTPException(status_code=503, detail="Evaluator not available")
    
    try:
        return {
            "metrics": evaluator.metrics,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")


@app.get("/patients/high-risk")
async def get_high_risk_patients(limit: int = 10):
    """Get list of high-risk patients"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        query = f"""
            SELECT 
                dp.patient_id,
                dp.age,
                dp.chronic_condition_count,
                COUNT(fv.visit_id) as visit_count,
                SUM(fv.is_admitted) as admission_count
            FROM dim_patient dp
            JOIN fact_visits fv ON dp.patient_id = fv.patient_id
            WHERE dp.chronic_condition_count >= 2
            GROUP BY dp.patient_id, dp.age, dp.chronic_condition_count
            ORDER BY dp.chronic_condition_count DESC, admission_count DESC
            LIMIT {limit}
        """
        
        result = db_connection.execute(query).df()
        
        patients = []
        for _, row in result.iterrows():
            patients.append({
                "patient_id": row['patient_id'],
                "age": int(row['age']),
                "chronic_condition_count": int(row['chronic_condition_count']),
                "visit_count": int(row['visit_count']),
                "admission_count": int(row['admission_count'])
            })
        
        return {
            "high_risk_patients": patients,
            "count": len(patients),
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching high-risk patients: {str(e)}")


@app.get("/opd-analytics")
async def get_opd_analytics():
    """Get OPD (Outpatient) analytics"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Load processed data for detailed OPD analysis
        processed_visits_path = 'backend/data/processed/visits_clean.parquet'
        if not os.path.exists(processed_visits_path):
            raise HTTPException(status_code=404, detail="Processed data not found")
            
        df_visits = pd.read_parquet(processed_visits_path)
        
        # Filter for outpatient visits only
        df_opd = df_visits[df_visits['is_admitted'] == False]
        
        # Wait times by department
        dept_wait = df_opd.groupby('department').agg({
            'wait_time_minutes': 'mean',
            'visit_id': 'count'
        }).reset_index()
        dept_wait.columns = ['department', 'avg_wait_time', 'visit_count']
        dept_wait = dept_wait.sort_values('avg_wait_time', ascending=False)
        dept_wait_list = dept_wait.to_dict('records')
        
        # Wait times by hour of day
        hourly = df_opd.groupby('hour_of_day').agg({
            'wait_time_minutes': 'mean'
        }).reset_index()
        hourly.columns = ['hour_of_day', 'avg_wait_time']
        hourly = hourly.sort_values('hour_of_day')
        hourly_list = hourly.to_dict('records')
        
        # Wait times by day of week
        daily = df_opd.groupby('day_of_week').agg({
            'wait_time_minutes': 'mean',
            'visit_id': 'count'
        }).reset_index()
        daily.columns = ['day_of_week', 'avg_wait_time', 'visit_count']
        daily = daily.sort_values('day_of_week')
        daily_list = daily.to_dict('records')
        
        return {
            "wait_times_by_department": dept_wait_list,
            "wait_times_by_hour": hourly_list,
            "wait_times_by_day": daily_list,
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching OPD analytics: {str(e)}")


@app.get("/inpatient-analytics")
async def get_inpatient_analytics():
    """Get Inpatient analytics"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Load processed data for more detailed analysis
        processed_visits_path = 'backend/data/processed/visits_clean.parquet'
        if os.path.exists(processed_visits_path):
            df_visits = pd.read_parquet(processed_visits_path)
            
            # LOS by ward
            ward_los = df_visits[df_visits['is_admitted'] == True].groupby('ward').agg({
                'length_of_stay_days': 'mean',
                'visit_id': 'count'
            }).reset_index()
            ward_los.columns = ['ward', 'avg_los', 'admission_count']
            ward_los = ward_los.to_dict('records')
            
            # Readmissions by diagnosis
            readmit_by_diag = df_visits[df_visits['is_admitted'] == True].groupby('diagnosis_code').agg({
                'readmitted_30d_flag': ['sum', 'count']
            }).reset_index()
            readmit_by_diag.columns = ['diagnosis_code', 'readmissions', 'total_admissions']
            readmit_by_diag['readmission_rate'] = (readmit_by_diag['readmissions'] / readmit_by_diag['total_admissions'] * 100).round(2)
            readmit_by_diag = readmit_by_diag.to_dict('records')
            
            # Monthly admission trends
            df_visits['visit_date'] = pd.to_datetime(df_visits['visit_date'])
            df_visits['month'] = df_visits['visit_date'].dt.to_period('M').astype(str)
            monthly_admissions = df_visits[df_visits['is_admitted'] == True].groupby('month').size().reset_index()
            monthly_admissions.columns = ['month', 'admission_count']
            monthly_admissions = monthly_admissions.to_dict('records')
            
        else:
            ward_los = []
            readmit_by_diag = []
            monthly_admissions = []
        
        return {
            "los_by_ward": ward_los,
            "readmissions_by_diagnosis": readmit_by_diag,
            "monthly_admission_trends": monthly_admissions,
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inpatient analytics: {str(e)}")


@app.get("/patients/list")
async def get_patient_list(limit: int = 1000):
    """Get list of patients with details for risk assessment"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Load processed data for comprehensive patient profiles
        patients_path = 'backend/data/processed/patients_clean.parquet'
        visits_path = 'backend/data/processed/visits_clean.parquet'
        
        if os.path.exists(patients_path) and os.path.exists(visits_path):
            df_patients = pd.read_parquet(patients_path)
            df_visits = pd.read_parquet(visits_path)
            
            # Calculate patient statistics
            patient_stats = df_visits.groupby('patient_id').agg({
                'visit_id': 'count',
                'is_admitted': 'sum',
                'length_of_stay_days': 'mean'
            }).reset_index()
            patient_stats.columns = ['patient_id', 'total_visits', 'total_admissions', 'avg_los']
            
            # Merge with patient data
            patients_full = df_patients.merge(patient_stats, on='patient_id', how='left')
            patients_full = patients_full.fillna(0)
            
            # Extract chronic conditions
            patients_full['has_diabetes'] = patients_full['chronic_conditions'].str.contains('Diabetes', na=False).astype(int)
            patients_full['has_hypertension'] = patients_full['chronic_conditions'].str.contains('Hypertension', na=False).astype(int)
            patients_full['has_asthma'] = patients_full['chronic_conditions'].str.contains('Asthma', na=False).astype(int)
            patients_full['has_heart_disease'] = patients_full['chronic_conditions'].str.contains('Heart Disease', na=False).astype(int)
            
            # Select top patients
            patients_list = patients_full.head(limit)
            
            patients_data = []
            for _, row in patients_list.iterrows():
                patients_data.append({
                    "patient_id": row['patient_id'],
                    "age": int(row['age']),
                    "gender": row['gender'],
                    "bmi": float(row['bmi']),
                    "smoking_status": row['smoking_status'],
                    "chronic_condition_count": int(row['chronic_condition_count']),
                    "chronic_conditions": row['chronic_conditions'],
                    "has_diabetes": int(row['has_diabetes']),
                    "has_hypertension": int(row['has_hypertension']),
                    "has_asthma": int(row['has_asthma']),
                    "has_heart_disease": int(row['has_heart_disease']),
                    "total_visits": int(row['total_visits']),
                    "total_admissions": int(row['total_admissions']),
                    "avg_los": round(float(row['avg_los']), 1)
                })
            
            return {
                "patients": patients_data,
                "total_count": len(patients_data),
                "generated_at": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Patient data not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patient list: {str(e)}")


@app.get("/billing-summary")
async def get_billing_summary():
    """Get billing and revenue summary"""
    if db_connection is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Load visits data
        visits_path = 'backend/data/processed/visits_clean.parquet'
        if os.path.exists(visits_path):
            df_visits = pd.read_parquet(visits_path)
            
            total_revenue = df_visits['billing_amount'].sum()
            avg_billing = df_visits['billing_amount'].mean()
            
            # Revenue by department
            dept_revenue = df_visits.groupby('department')['billing_amount'].sum().sort_values(ascending=False).to_dict()
            
            return {
                "total_revenue": round(float(total_revenue), 2),
                "average_billing_per_visit": round(float(avg_billing), 2),
                "revenue_by_department": dept_revenue,
                "generated_at": datetime.now().isoformat()
            }
        else:
            return {
                "total_revenue": 0,
                "average_billing_per_visit": 0,
                "revenue_by_department": {},
                "generated_at": datetime.now().isoformat()
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching billing summary: {str(e)}")


# Run with: uvicorn api:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
