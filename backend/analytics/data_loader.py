"""
Data Loader Module
Handles loading and basic validation of hospital datasets
"""

import pandas as pd
import os


class DataLoader:
    """Load and validate hospital datasets"""
    
    def __init__(self, data_dir='backend/data/raw'):
        """
        Initialize data loader
        
        Args:
            data_dir: Directory containing raw data files
        """
        self.data_dir = data_dir
        
    def load_patients(self):
        """Load patient demographic data"""
        file_path = f'{self.data_dir}/patients.parquet'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Patients data not found at {file_path}")
        
        df = pd.read_parquet(file_path)
        print(f"✅ Loaded {len(df):,} patient records")
        return df
    
    def load_visits(self):
        """Load hospital visit data"""
        file_path = f'{self.data_dir}/visits.parquet'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Visits data not found at {file_path}")
        
        df = pd.read_parquet(file_path)
        print(f"✅ Loaded {len(df):,} visit records")
        return df
    
    def load_admissions(self):
        """Load admission data"""
        file_path = f'{self.data_dir}/admissions.parquet'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Admissions data not found at {file_path}")
        
        df = pd.read_parquet(file_path)
        print(f"✅ Loaded {len(df):,} admission records")
        return df
    
    def load_all(self):
        """Load all datasets"""
        print("\n🔄 Loading hospital datasets...")
        patients = self.load_patients()
        visits = self.load_visits()
        admissions = self.load_admissions()
        print("✅ All datasets loaded successfully\n")
        return patients, visits, admissions
    
    def validate_data(self, df_patients, df_visits, df_admissions):
        """Basic data validation"""
        print("🔍 Validating data integrity...")
        
        # Check for nulls
        for name, df in [('patients', df_patients), ('visits', df_visits), ('admissions', df_admissions)]:
            null_counts = df.isnull().sum()
            if null_counts.sum() > 0:
                print(f"⚠️  {name} has null values:\n{null_counts[null_counts > 0]}")
        
        # Check referential integrity
        patient_ids_in_visits = set(df_visits['patient_id'])
        patient_ids = set(df_patients['patient_id'])
        
        if not patient_ids_in_visits.issubset(patient_ids):
            print("❌ Referential integrity issue: Some visits reference non-existent patients")
        else:
            print("✅ Referential integrity validated")
        
        return True


if __name__ == '__main__':
    loader = DataLoader()
    patients, visits, admissions = loader.load_all()
    loader.validate_data(patients, visits, admissions)
