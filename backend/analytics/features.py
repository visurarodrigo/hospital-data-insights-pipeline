"""
Feature Engineering Module
Creates ML-ready features for predictive modeling
"""

import pandas as pd
import numpy as np


class FeatureEngineer:
    """Creates features for machine learning models"""
    
    def __init__(self):
        self.feature_names = []
    
    def create_patient_features(self, df_patients):
        """Create patient-level features"""
        df = df_patients.copy()
        
        # Age groups
        df['age_group'] = pd.cut(
            df['age'], 
            bins=[0, 18, 35, 50, 65, 100],
            labels=['Child', 'Young Adult', 'Adult', 'Senior', 'Elderly']
        )
        
        # BMI categories
        df['bmi_category'] = pd.cut(
            df['bmi'],
            bins=[0, 18.5, 25, 30, 100],
            labels=['Underweight', 'Normal', 'Overweight', 'Obese']
        )
        
        # Risk flags
        df['high_bmi'] = (df['bmi'] >= 30).astype(int)
        df['senior_citizen'] = (df['age'] >= 65).astype(int)
        df['multiple_conditions'] = (df['chronic_condition_count'] >= 2).astype(int)
        
        return df
    
    def create_visit_aggregations(self, df_visits):
        """Create patient visit history aggregations"""
        print("🔄 Creating visit aggregation features...")
        
        # Group by patient
        visit_agg = df_visits.groupby('patient_id').agg({
            'visit_id': 'count',
            'wait_time_minutes': 'mean',
            'is_admitted': 'sum',
            'satisfaction_score': 'mean',
            'visit_date': ['min', 'max']
        }).reset_index()
        
        visit_agg.columns = [
            'patient_id', 'total_visits', 'avg_wait_time', 
            'total_admissions', 'avg_satisfaction',
            'first_visit', 'last_visit'
        ]
        
        # Visit frequency
        visit_agg['days_since_first_visit'] = (
            visit_agg['last_visit'] - visit_agg['first_visit']
        ).dt.days + 1
        
        visit_agg['visit_frequency'] = (
            visit_agg['total_visits'] / visit_agg['days_since_first_visit'] * 365
        ).fillna(0)
        
        # Admission rate
        visit_agg['admission_rate'] = (
            visit_agg['total_admissions'] / visit_agg['total_visits']
        )
        
        # Frequent visitor flag
        visit_agg['frequent_visitor'] = (visit_agg['total_visits'] >= 5).astype(int)
        
        print(f"✅ Created aggregations for {len(visit_agg):,} patients")
        return visit_agg
    
    def create_readmission_features(self, df_visits):
        """Create features for readmission prediction"""
        print("🔄 Creating readmission prediction features...")
        
        # Filter only admitted patients
        df_admitted = df_visits[df_visits['is_admitted'] == 1].copy()
        
        # Sort by patient and date
        df_admitted = df_admitted.sort_values(['patient_id', 'visit_date'])
        
        # Count prior admissions
        df_admitted['prior_admissions'] = df_admitted.groupby('patient_id').cumcount()
        
        # Days since last admission
        df_admitted['days_since_last_admission'] = df_admitted.groupby('patient_id')['visit_date'].diff().dt.days
        df_admitted['days_since_last_admission'].fillna(0, inplace=True)
        
        # Recent admission flag (within 90 days)
        df_admitted['recent_admission'] = (df_admitted['days_since_last_admission'] <= 90).astype(int)
        
        print(f"✅ Created readmission features for {len(df_admitted):,} admissions")
        return df_admitted
    
    def create_ml_dataset(self, df_patients, df_visits):
        """Create complete ML-ready dataset"""
        print("\n" + "="*60)
        print("🔧 FEATURE ENGINEERING PIPELINE")
        print("="*60 + "\n")
        
        # Enhance patient features
        df_patients_enhanced = self.create_patient_features(df_patients)
        
        # Create visit aggregations
        visit_agg = self.create_visit_aggregations(df_visits)
        
        # Merge patients with visit history
        df_ml = df_patients_enhanced.merge(visit_agg, on='patient_id', how='left')
        
        # Fill missing values for patients with no visits
        df_ml['total_visits'].fillna(0, inplace=True)
        df_ml['total_admissions'].fillna(0, inplace=True)
        df_ml['avg_wait_time'].fillna(df_ml['avg_wait_time'].median(), inplace=True)
        df_ml['visit_frequency'].fillna(0, inplace=True)
        df_ml['admission_rate'].fillna(0, inplace=True)
        df_ml['frequent_visitor'].fillna(0, inplace=True)
        
        print(f"\n✅ ML dataset created: {len(df_ml):,} records")
        print(f"✅ Total features: {len(df_ml.columns)}")
        
        return df_ml
    
    def prepare_classification_features(self, df_ml):
        """Prepare features for readmission classification"""
        print("\n🔄 Preparing classification features...")
        
        # Select numeric features for modeling
        feature_cols = [
            'age', 'bmi', 'chronic_condition_count',
            'total_visits', 'total_admissions', 'avg_wait_time',
            'visit_frequency', 'admission_rate',
            'is_smoker', 'has_chronic_condition',
            'high_bmi', 'senior_citizen', 'multiple_conditions',
            'frequent_visitor'
        ]
        
        # Filter to patients with at least one admission
        df_filtered = df_ml[df_ml['total_admissions'] > 0].copy()
        
        # Create target: high readmission risk
        # Based on admission rate and visit frequency
        df_filtered['high_readmission_risk'] = (
            (df_filtered['admission_rate'] >= 0.3) | 
            (df_filtered['total_admissions'] >= 2)
        ).astype(int)
        
        X = df_filtered[feature_cols].fillna(0)
        y = df_filtered['high_readmission_risk']
        
        print(f"✅ Classification dataset: {len(X):,} samples")
        print(f"✅ Positive class (high risk): {y.sum():,} ({y.mean()*100:.1f}%)")
        print(f"✅ Features: {len(feature_cols)}")
        
        self.feature_names = feature_cols
        
        return X, y, df_filtered
    
    def prepare_regression_features(self, df_visits):
        """Prepare features for wait time prediction"""
        print("\n🔄 Preparing regression features...")
        
        df = df_visits.copy()
        
        # Create time-based features
        df['hour'] = df['visit_date'].dt.hour
        df['day_of_week'] = df['visit_date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_emergency'] = (df['department'] == 'Emergency').astype(int)
        
        # Department encoding (one-hot)
        dept_dummies = pd.get_dummies(df['department'], prefix='dept')
        df = pd.concat([df, dept_dummies], axis=1)
        
        # Feature columns
        feature_cols = ['hour', 'day_of_week', 'is_weekend', 'is_emergency'] + list(dept_dummies.columns)
        
        X = df[feature_cols]
        y = df['wait_time_minutes']
        
        print(f"✅ Regression dataset: {len(X):,} samples")
        print(f"✅ Features: {len(feature_cols)}")
        print(f"✅ Target range: {y.min():.1f} - {y.max():.1f} minutes")
        
        return X, y, df
    
    def save_features(self, df_ml, output_path='backend/data/processed/ml_features.parquet'):
        """Save engineered features"""
        df_ml.to_parquet(output_path, index=False)
        print(f"\n💾 Features saved to {output_path}")


if __name__ == '__main__':
    from data_loader import DataLoader
    
    loader = DataLoader(data_dir='backend/data/processed')
    patients, visits, admissions = loader.load_all()
    
    engineer = FeatureEngineer()
    df_ml = engineer.create_ml_dataset(patients, visits)
    
    # Prepare classification features
    X_class, y_class, df_class = engineer.prepare_classification_features(df_ml)
    print(f"\nClassification features shape: {X_class.shape}")
    print(f"Feature names: {engineer.feature_names}")
    
    # Prepare regression features
    X_reg, y_reg, df_reg = engineer.prepare_regression_features(visits)
    print(f"\nRegression features shape: {X_reg.shape}")
    
    # Save
    engineer.save_features(df_ml)
