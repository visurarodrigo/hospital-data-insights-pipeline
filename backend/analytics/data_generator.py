"""
Synthetic Healthcare Data Generator
Generates realistic hospital datasets for analytics pipeline
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)


class HospitalDataGenerator:
    """Generates synthetic hospital data for testing and development"""
    
    def __init__(self, n_patients=5000, n_visits=15000):
        """
        Initialize data generator
        
        Args:
            n_patients: Number of unique patients to generate
            n_visits: Number of hospital visits to generate
        """
        self.n_patients = n_patients
        self.n_visits = n_visits
        self.departments = [
            'Cardiology', 'Orthopedics', 'Neurology', 
            'Pediatrics', 'Emergency', 'General Medicine',
            'Surgery', 'Oncology', 'Psychiatry', 'Dermatology'
        ]
        self.chronic_conditions = [
            'Diabetes', 'Hypertension', 'Asthma', 'Heart Disease',
            'Kidney Disease', 'COPD', 'Arthritis', 'None'
        ]
        self.wards = ['Ward A', 'Ward B', 'Ward C', 'Ward D', 'ICU', 'CCU', 'NICU', 'Pediatric Ward']
        self.diagnosis_codes = ['I10', 'E11', 'J44', 'I25', 'N18', 'M15', 'F32', 'C34', 'J18', 'I50']
        self.triage_levels = ['Level 1 - Resuscitation', 'Level 2 - Emergency', 'Level 3 - Urgent', 'Level 4 - Semi-urgent', 'Level 5 - Non-urgent']
        
    def generate_patients(self):
        """Generate patient demographic data"""
        print("🔄 Generating patient data...")
        
        patients = []
        for patient_id in range(1, self.n_patients + 1):
            age = np.random.randint(1, 95)
            gender = random.choice(['M', 'F', 'Other'])
            
            # Age and gender affect BMI distribution
            if age < 18:
                bmi = np.random.normal(18, 3)
            else:
                bmi = np.random.normal(26, 5)
            
            bmi = max(15, min(45, bmi))  # Cap BMI between 15-45
            
            # Smoking more likely in adults
            smoking_status = 'Yes' if (age >= 18 and random.random() < 0.25) else 'No'
            
            # Chronic conditions increase with age
            chronic_prob = min(0.7, age / 100)
            n_conditions = np.random.binomial(3, chronic_prob)
            conditions = random.sample(
                [c for c in self.chronic_conditions if c != 'None'], 
                min(n_conditions, len(self.chronic_conditions) - 1)
            ) if n_conditions > 0 else ['None']
            
            patients.append({
                'patient_id': f'P{patient_id:05d}',
                'age': int(age),
                'gender': gender,
                'bmi': round(bmi, 1),
                'smoking_status': smoking_status,
                'chronic_conditions': ', '.join(conditions),
                'chronic_condition_count': len([c for c in conditions if c != 'None']),
                'registration_date': fake.date_between(start_date='-5y', end_date='today')
            })
        
        df_patients = pd.DataFrame(patients)
        print(f"✅ Generated {len(df_patients)} patients")
        return df_patients
    
    def generate_visits(self, df_patients):
        """Generate hospital visit records"""
        print("🔄 Generating visit data...")
        
        visits = []
        patient_ids = df_patients['patient_id'].tolist()
        
        # Some patients visit more frequently
        visit_distribution = np.random.zipf(1.5, self.n_visits)
        visit_distribution = visit_distribution % len(patient_ids)
        
        for visit_id in range(1, self.n_visits + 1):
            patient_id = patient_ids[visit_distribution[visit_id - 1]]
            patient_data = df_patients[df_patients['patient_id'] == patient_id].iloc[0]
            
            visit_date = fake.date_time_between(start_date='-2y', end_date='now')
            department = random.choice(self.departments)
            visit_type = 'Emergency' if department == 'Emergency' else random.choice(['OPD', 'Scheduled'])
            
            # Triage level (emergency gets 1-3, others get 3-5)
            if visit_type == 'Emergency':
                triage = random.choice(self.triage_levels[:3])
            else:
                triage = random.choice(self.triage_levels[2:])
            
            # Hour and day of week
            hour_of_day = visit_date.hour
            day_of_week = visit_date.weekday()
            
            # Wait time varies by department, triage, and time
            base_wait = 45
            if visit_type == 'Emergency':
                base_wait = 15 if 'Level 1' in triage else 25
            elif department == 'Emergency':
                base_wait = 20
            
            # Peak hours increase wait time
            if 9 <= hour_of_day <= 16:
                base_wait *= 1.3
            
            wait_time = max(5, np.random.normal(base_wait, base_wait * 0.4))
            
            # Admission probability based on age and conditions
            admission_prob = 0.15 + (patient_data['age'] / 200) + (patient_data['chronic_condition_count'] * 0.05)
            if visit_type == 'Emergency':
                admission_prob *= 1.5
            is_admitted = random.random() < min(0.8, admission_prob)
            
            # Ward assignment if admitted
            ward = None
            if is_admitted:
                if patient_data['age'] < 18:
                    ward = 'Pediatric Ward'
                elif department == 'Cardiology':
                    ward = 'CCU' if random.random() < 0.3 else random.choice(['Ward A', 'Ward B'])
                elif visit_type == 'Emergency' and 'Level 1' in triage:
                    ward = 'ICU'
                else:
                    ward = random.choice(self.wards[:4])
            
            # Length of stay if admitted
            if is_admitted:
                los = max(1, int(np.random.exponential(4)))
            else:
                los = 0
            
            # Diagnosis code
            diagnosis_code = random.choice(self.diagnosis_codes)
            
            # Readmission within 30 days (for admitted patients)
            readmitted_30d_flag = 1 if (is_admitted and random.random() < 0.18) else 0
            
            # Billing amount
            base_billing = 500 if visit_type == 'OPD' else 1500
            billing = base_billing + (los * 1200) + np.random.normal(0, 200)
            
            visits.append({
                'visit_id': f'V{visit_id:06d}',
                'patient_id': patient_id,
                'visit_date': visit_date,
                'department': department,
                'visit_type': visit_type,
                'triage_level': triage,
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'wait_time_minutes': round(wait_time, 1),
                'is_admitted': is_admitted,
                'ward': ward if is_admitted else None,
                'diagnosis_code': diagnosis_code if is_admitted else None,
                'length_of_stay_days': los,
                'readmitted_30d_flag': readmitted_30d_flag,
                'satisfaction_score': np.random.randint(1, 6),  # 1-5 scale
                'billing_amount': round(max(0, billing), 2)
            })
        
        df_visits = pd.DataFrame(visits)
        print(f"✅ Generated {len(df_visits)} visits")
        return df_visits
    
    def generate_admissions(self, df_visits):
        """Generate detailed admission records from visits"""
        print("🔄 Generating admission data...")
        
        admissions = df_visits[df_visits['is_admitted'] == True].copy()
        admissions['admission_id'] = [f'A{i:05d}' for i in range(1, len(admissions) + 1)]
        admissions['discharge_date'] = admissions.apply(
            lambda row: row['visit_date'] + timedelta(days=row['length_of_stay_days']),
            axis=1
        )
        admissions['discharge_status'] = admissions['readmitted_30d_flag'].apply(
            lambda x: 'Readmitted' if x == 1 else random.choice(['Improved', 'Recovered', 'Stable'])
        )
        
        print(f"✅ Generated {len(admissions)} admissions")
        return admissions[['admission_id', 'visit_id', 'patient_id', 'visit_date', 
                           'discharge_date', 'ward', 'diagnosis_code', 'length_of_stay_days', 
                           'discharge_status', 'readmitted_30d_flag', 'billing_amount']]
    
    def save_data(self, output_dir='backend/data/raw'):
        """Generate and save all datasets"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*60)
        print("🏥 HOSPITAL DATA GENERATION PIPELINE")
        print("="*60 + "\n")
        
        # Generate data
        df_patients = self.generate_patients()
        df_visits = self.generate_visits(df_patients)
        df_admissions = self.generate_admissions(df_visits)
        
        # Save to parquet format
        print("\n🔄 Saving datasets...")
        df_patients.to_parquet(f'{output_dir}/patients.parquet', index=False)
        df_visits.to_parquet(f'{output_dir}/visits.parquet', index=False)
        df_admissions.to_parquet(f'{output_dir}/admissions.parquet', index=False)
        
        print(f"✅ Saved to {output_dir}/")
        print("\n" + "="*60)
        print("📊 DATA SUMMARY")
        print("="*60)
        print(f"Patients:   {len(df_patients):,}")
        print(f"Visits:     {len(df_visits):,}")
        print(f"Admissions: {len(df_admissions):,}")
        print(f"Admission Rate: {len(df_admissions)/len(df_visits)*100:.1f}%")
        print("="*60 + "\n")
        
        return df_patients, df_visits, df_admissions


if __name__ == '__main__':
    generator = HospitalDataGenerator(n_patients=5000, n_visits=15000)
    generator.save_data()
