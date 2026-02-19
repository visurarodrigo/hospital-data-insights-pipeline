"""
Prediction Service
Makes predictions using trained models
"""

import pandas as pd
import numpy as np
import joblib
import os
import json


class PredictionService:
    """Makes predictions for readmission risk and wait times"""
    
    def __init__(self, model_dir='backend/models'):
        """
        Initialize prediction service
        
        Args:
            model_dir: Directory containing trained models
        """
        self.model_dir = model_dir
        self.classifier = None
        self.regressor = None
        self.scaler_class = None
        self.scaler_reg = None
        self.feature_names_class = None
        self.feature_names_reg = None
        
        self.load_models()
    
    def load_models(self):
        """Load all trained models and scalers"""
        try:
            self.classifier = joblib.load(f'{self.model_dir}/classifier.pkl')
            self.scaler_class = joblib.load(f'{self.model_dir}/scaler_classifier.pkl')
            print("✅ Classification model loaded")
        except Exception as e:
            print(f"⚠️  Could not load classifier: {e}")
        
        try:
            self.regressor = joblib.load(f'{self.model_dir}/regressor.pkl')
            self.scaler_reg = joblib.load(f'{self.model_dir}/scaler_regressor.pkl')
            print("✅ Regression model loaded")
        except Exception as e:
            print(f"⚠️  Could not load regressor: {e}")
        
        try:
            with open(f'{self.model_dir}/metrics.json', 'r') as f:
                self.metrics = json.load(f)
        except:
            self.metrics = {}
    
    def predict_readmission_risk(self, patient_features):
        """
        Predict readmission risk for a patient
        
        Args:
            patient_features: Dict or DataFrame with patient features
        
        Returns:
            Dict with risk probability and classification
        """
        if self.classifier is None:
            raise ValueError("Classifier not loaded")
        
        # Convert to DataFrame if dict
        if isinstance(patient_features, dict):
            patient_features = pd.DataFrame([patient_features])
        
        # Expected features for classification
        expected_features = [
            'age', 'bmi', 'chronic_condition_count',
            'total_visits', 'total_admissions', 'avg_wait_time',
            'visit_frequency', 'admission_rate',
            'is_smoker', 'has_chronic_condition',
            'high_bmi', 'senior_citizen', 'multiple_conditions',
            'frequent_visitor'
        ]
        
        # Ensure all features are present
        for feat in expected_features:
            if feat not in patient_features.columns:
                patient_features[feat] = 0
        
        X = patient_features[expected_features]
        
        # Scale features
        X_scaled = self.scaler_class.transform(X)
        
        # Predict
        risk_proba = self.classifier.predict_proba(X_scaled)[:, 1][0]
        risk_class = 'High Risk' if risk_proba >= 0.5 else 'Low Risk'
        
        return {
            'risk_probability': float(risk_proba),
            'risk_class': risk_class,
            'risk_level': self._get_risk_level(risk_proba)
        }
    
    def _get_risk_level(self, probability):
        """Convert probability to risk level"""
        if probability >= 0.7:
            return 'Very High'
        elif probability >= 0.5:
            return 'High'
        elif probability >= 0.3:
            return 'Moderate'
        else:
            return 'Low'
    
    def predict_wait_time(self, visit_features):
        """
        Predict wait time for a visit
        
        Args:
            visit_features: Dict or DataFrame with visit features
        
        Returns:
            Predicted wait time in minutes
        """
        if self.regressor is None:
            raise ValueError("Regressor not loaded")
        
        # Convert to DataFrame if dict
        if isinstance(visit_features, dict):
            visit_features = pd.DataFrame([visit_features])
        
        # Scale features
        X_scaled = self.scaler_reg.transform(visit_features)
        
        # Predict
        wait_time = self.regressor.predict(X_scaled)[0]
        
        return {
            'predicted_wait_time_minutes': float(max(0, wait_time)),
            'predicted_wait_time_formatted': self._format_wait_time(wait_time)
        }
    
    def _format_wait_time(self, minutes):
        """Format wait time for display"""
        if minutes < 60:
            return f"{int(minutes)} minutes"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h {mins}m"
    
    def get_model_info(self):
        """Get information about loaded models"""
        return {
            'classifier_loaded': self.classifier is not None,
            'regressor_loaded': self.regressor is not None,
            'metrics': self.metrics
        }


if __name__ == '__main__':
    # Test prediction service
    service = PredictionService()
    
    # Test readmission risk prediction
    test_patient = {
        'age': 65,
        'bmi': 32.5,
        'chronic_condition_count': 2,
        'total_visits': 8,
        'total_admissions': 3,
        'avg_wait_time': 45.0,
        'visit_frequency': 12.0,
        'admission_rate': 0.375,
        'is_smoker': 1,
        'has_chronic_condition': 1,
        'high_bmi': 1,
        'senior_citizen': 1,
        'multiple_conditions': 1,
        'frequent_visitor': 1
    }
    
    print("\n🧪 Testing Readmission Risk Prediction:")
    print(f"Patient: {test_patient}")
    result = service.predict_readmission_risk(test_patient)
    print(f"\nResult: {result}")
    
    print(f"\n📊 Model Info:")
    print(service.get_model_info())
