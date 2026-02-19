"""
ETL (Extract, Transform, Load) Module
Performs data cleaning and transformations
"""

import pandas as pd
import numpy as np
from datetime import datetime


class ETLProcessor:
    """Handles ETL operations for hospital data"""
    
    def __init__(self):
        self.transformations_applied = []
    
    def clean_patients(self, df):
        """Clean and transform patient data"""
        print("🔄 Cleaning patient data...")
        df = df.copy()
        
        # Handle missing values
        if df['bmi'].isnull().any():
            df['bmi'].fillna(df['bmi'].median(), inplace=True)
            self.transformations_applied.append("Filled missing BMI with median")
        
        # Standardize categorical values
        df['gender'] = df['gender'].str.upper()
        df['smoking_status'] = df['smoking_status'].str.capitalize()
        
        # Convert registration_date to datetime
        if not pd.api.types.is_datetime64_any_dtype(df['registration_date']):
            df['registration_date'] = pd.to_datetime(df['registration_date'])
        
        # Add derived fields
        df['is_smoker'] = (df['smoking_status'] == 'Yes').astype(int)
        df['has_chronic_condition'] = (df['chronic_condition_count'] > 0).astype(int)
        
        print(f"✅ Cleaned {len(df)} patient records")
        return df
    
    def clean_visits(self, df):
        """Clean and transform visit data"""
        print("🔄 Cleaning visit data...")
        df = df.copy()
        
        # Convert visit_date to datetime
        if not pd.api.types.is_datetime64_any_dtype(df['visit_date']):
            df['visit_date'] = pd.to_datetime(df['visit_date'])
        
        # Handle negative wait times
        df['wait_time_minutes'] = df['wait_time_minutes'].clip(lower=0)
        
        # Standardize categorical values
        df['department'] = df['department'].str.title()
        df['visit_type'] = df['visit_type'].str.title()
        
        # Convert boolean fields
        df['is_admitted'] = df['is_admitted'].astype(int)
        # readmitted_30d_flag is already an int from data generator
        if 'readmitted_30d' in df.columns:
            df['readmitted_30d_flag'] = (df['readmitted_30d'] == 'Yes').astype(int)
        
        # Extract date components
        df['visit_year'] = df['visit_date'].dt.year
        df['visit_month'] = df['visit_date'].dt.month
        df['visit_day'] = df['visit_date'].dt.day
        df['visit_weekday'] = df['visit_date'].dt.dayofweek
        df['visit_hour'] = df['visit_date'].dt.hour if 'hour_of_day' not in df.columns else df['visit_date'].dt.hour
        
        print(f"✅ Cleaned {len(df)} visit records")
        return df
    
    def clean_admissions(self, df):
        """Clean and transform admission data"""
        print("🔄 Cleaning admission data...")
        df = df.copy()
        
        # Convert dates to datetime
        if not pd.api.types.is_datetime64_any_dtype(df['visit_date']):
            df['visit_date'] = pd.to_datetime(df['visit_date'])
        if not pd.api.types.is_datetime64_any_dtype(df['discharge_date']):
            df['discharge_date'] = pd.to_datetime(df['discharge_date'])
        
        # Standardize categorical values
        df['discharge_status'] = df['discharge_status'].str.title()
        
        # Add derived fields if needed
        if 'readmitted_30d' in df.columns:
            df['readmitted_30d_flag'] = (df['readmitted_30d'] == 'Yes').astype(int)
        # else readmitted_30d_flag already exists from data generator
        
        print(f"✅ Cleaned {len(df)} admission records")
        return df
    
    def merge_patient_visits(self, df_patients, df_visits):
        """Merge patient and visit data for analysis"""
        print("🔄 Merging patient and visit data...")
        
        df_merged = df_visits.merge(
            df_patients,
            on='patient_id',
            how='left'
        )
        
        print(f"✅ Merged dataset contains {len(df_merged)} records")
        return df_merged
    
    def process_all(self, df_patients, df_visits, df_admissions):
        """Run full ETL pipeline"""
        print("\n" + "="*60)
        print("🔄 ETL PIPELINE STARTED")
        print("="*60 + "\n")
        
        df_patients_clean = self.clean_patients(df_patients)
        df_visits_clean = self.clean_visits(df_visits)
        df_admissions_clean = self.clean_admissions(df_admissions)
        
        print("\n✅ ETL Pipeline completed successfully\n")
        
        return df_patients_clean, df_visits_clean, df_admissions_clean
    
    def save_processed_data(self, df_patients, df_visits, df_admissions, output_dir='backend/data/processed'):
        """Save processed data"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("💾 Saving processed data...")
        df_patients.to_parquet(f'{output_dir}/patients_clean.parquet', index=False)
        df_visits.to_parquet(f'{output_dir}/visits_clean.parquet', index=False)
        df_admissions.to_parquet(f'{output_dir}/admissions_clean.parquet', index=False)
        
        print(f"✅ Saved to {output_dir}/\n")


if __name__ == '__main__':
    from data_loader import DataLoader
    
    loader = DataLoader()
    patients, visits, admissions = loader.load_all()
    
    etl = ETLProcessor()
    patients_clean, visits_clean, admissions_clean = etl.process_all(patients, visits, admissions)
    etl.save_processed_data(patients_clean, visits_clean, admissions_clean)
