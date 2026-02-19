"""
Hospital Data Insights Pipeline Runner
Executes the complete data pipeline from generation to model training
"""

import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append('backend')

from analytics.data_generator import HospitalDataGenerator
from analytics.data_loader import DataLoader
from analytics.etl import ETLProcessor
from analytics.features import FeatureEngineer
from analytics.models import ModelTrainer
from warehouse.build_db import WarehouseBuilder


def print_banner(text):
    """Print a decorative banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def run_complete_pipeline():
    """Execute the complete data pipeline"""
    start_time = datetime.now()
    
    print_banner("🏥 HOSPITAL DATA INSIGHTS PIPELINE")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Generate synthetic data
        print_banner("STEP 1: GENERATING SYNTHETIC DATA")
        generator = HospitalDataGenerator(n_patients=5000, n_visits=15000)
        df_patients_raw, df_visits_raw, df_admissions_raw = generator.save_data()
        
        # Step 2: Load and validate data
        print_banner("STEP 2: LOADING & VALIDATING DATA")
        loader = DataLoader()
        df_patients, df_visits, df_admissions = loader.load_all()
        loader.validate_data(df_patients, df_visits, df_admissions)
        
        # Step 3: ETL Processing
        print_banner("STEP 3: ETL PROCESSING")
        etl = ETLProcessor()
        df_patients_clean, df_visits_clean, df_admissions_clean = etl.process_all(
            df_patients, df_visits, df_admissions
        )
        etl.save_processed_data(df_patients_clean, df_visits_clean, df_admissions_clean)
        
        # Step 4: Build Data Warehouse
        print_banner("STEP 4: BUILDING DATA WAREHOUSE")
        warehouse = WarehouseBuilder()
        warehouse.build_warehouse(df_patients_clean, df_visits_clean)
        warehouse.run_sample_queries()
        warehouse.close()
        
        # Step 5: Feature Engineering
        print_banner("STEP 5: FEATURE ENGINEERING")
        engineer = FeatureEngineer()
        df_ml = engineer.create_ml_dataset(df_patients_clean, df_visits_clean)
        engineer.save_features(df_ml)
        
        # Prepare features for modeling
        X_class, y_class, df_class = engineer.prepare_classification_features(df_ml)
        X_reg, y_reg, df_reg = engineer.prepare_regression_features(df_visits_clean)
        
        # Step 6: Train Machine Learning Models
        print_banner("STEP 6: TRAINING ML MODELS")
        trainer = ModelTrainer()
        
        # Train classifier (with TabPFN priority)
        trainer.train_classifier(X_class, y_class, use_tabpfn=True)
        
        # Train regressor
        trainer.train_regressor(X_reg, y_reg)
        
        # Save models
        trainer.save_models()
        
        # Step 7: Pipeline Complete
        print_banner("✅ PIPELINE COMPLETED SUCCESSFULLY")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        print("\n📁 Generated Files:")
        print("  • Raw data: backend/data/raw/*.parquet")
        print("  • Processed data: backend/data/processed/*.parquet")
        print("  • DuckDB warehouse: backend/data/hospital_warehouse.db")
        print("  • Trained models: backend/models/*.pkl")
        print("  • Model metrics: backend/models/metrics.json")
        
        print("\n🚀 Next Steps:")
        print("  1. Start API server: uvicorn backend.api:app --reload")
        print("  2. Open frontend: Open frontend/index.html in browser")
        print("  3. View API docs: http://localhost:8000/docs")
        
        print("\n" + "="*70 + "\n")
        
        return True
        
    except Exception as e:
        print_banner("❌ PIPELINE FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_complete_pipeline()
    sys.exit(0 if success else 1)
