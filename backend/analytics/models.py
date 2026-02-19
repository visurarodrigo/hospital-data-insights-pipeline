"""
Machine Learning Model Training
Primary: TabPFN (Large Tabular Foundation Model)
Fallbacks: Random Forest, Logistic Regression
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, mean_squared_error, r2_score
)
import joblib
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Trains and evaluates ML models with TabPFN priority"""
    
    def __init__(self, model_dir='backend/models'):
        """
        Initialize model trainer
        
        Args:
            model_dir: Directory to save trained models
        """
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        self.classifier = None
        self.regressor = None
        self.scaler_class = None
        self.scaler_reg = None
        self.metrics = {}
        self.model_type_used = None
    
    def _try_tabpfn_classifier(self):
        """Try to import and use TabPFN classifier"""
        try:
            from tabpfn import TabPFNClassifier
            print("✅ TabPFN available - using Large Tabular Foundation Model")
            return TabPFNClassifier(device='cpu', N_ensemble_configurations=4)
        except ImportError:
            print("⚠️  TabPFN not available, falling back to traditional models")
            return None
        except Exception as e:
            print(f"⚠️  TabPFN error: {e}, falling back to traditional models")
            return None
    
    def _get_fallback_classifier(self, model_preference='random_forest'):
        """Get fallback classifier"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        
        if model_preference == 'random_forest':
            print("📊 Using Random Forest Classifier (Fallback)")
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=20,
                min_samples_leaf=10,
                random_state=42,
                n_jobs=-1
            )
        else:
            print("📊 Using Logistic Regression (Baseline)")
            return LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            )
    
    def train_classifier(self, X, y, test_size=0.2, use_tabpfn=True):
        """
        Train readmission risk classifier
        
        Args:
            X: Feature matrix
            y: Target labels
            test_size: Test set proportion
            use_tabpfn: Whether to try TabPFN first
        
        Returns:
            Trained model and metrics
        """
        print("\n" + "="*60)
        print("🎯 TRAINING READMISSION RISK CLASSIFIER")
        print("="*60 + "\n")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"Training set: {len(X_train):,} samples")
        print(f"Test set: {len(X_test):,} samples")
        print(f"Positive class: {y_train.sum():,} ({y_train.mean()*100:.1f}%)\n")
        
        # Scale features
        self.scaler_class = StandardScaler()
        X_train_scaled = self.scaler_class.fit_transform(X_train)
        X_test_scaled = self.scaler_class.transform(X_test)
        
        # Try TabPFN first
        if use_tabpfn:
            tabpfn_model = self._try_tabpfn_classifier()
            if tabpfn_model is not None:
                try:
                    # TabPFN has limitations on dataset size
                    # Use subset if dataset is too large
                    max_samples = 1000
                    if len(X_train_scaled) > max_samples:
                        print(f"⚠️  Dataset too large for TabPFN, sampling {max_samples} records")
                        sample_idx = np.random.choice(len(X_train_scaled), max_samples, replace=False)
                        X_train_tabpfn = X_train_scaled[sample_idx]
                        y_train_tabpfn = y_train.iloc[sample_idx] if hasattr(y_train, 'iloc') else y_train[sample_idx]
                    else:
                        X_train_tabpfn = X_train_scaled
                        y_train_tabpfn = y_train
                    
                    print("🔄 Training TabPFN model...")
                    tabpfn_model.fit(X_train_tabpfn, y_train_tabpfn)
                    self.classifier = tabpfn_model
                    self.model_type_used = 'TabPFN'
                    print("✅ TabPFN training complete\n")
                except Exception as e:
                    print(f"⚠️  TabPFN training failed: {e}")
                    print("Falling back to Random Forest...\n")
                    self.classifier = None
        
        # Fallback to traditional models
        if self.classifier is None:
            self.classifier = self._get_fallback_classifier('random_forest')
            self.model_type_used = 'RandomForest'
            print("🔄 Training Random Forest model...")
            self.classifier.fit(X_train_scaled, y_train)
            print("✅ Random Forest training complete\n")
        
        # Evaluate
        y_pred = self.classifier.predict(X_test_scaled)
        y_pred_proba = self.classifier.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        metrics = {
            'model_type': self.model_type_used,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'features': X.shape[1],
            'timestamp': datetime.now().isoformat()
        }
        
        self.metrics['classifier'] = metrics
        
        # Print results
        print("📊 CLASSIFICATION RESULTS:")
        print(f"  Model Type: {metrics['model_type']}")
        print(f"  Accuracy:   {metrics['accuracy']:.4f}")
        print(f"  Precision:  {metrics['precision']:.4f}")
        print(f"  Recall:     {metrics['recall']:.4f}")
        print(f"  F1 Score:   {metrics['f1_score']:.4f}")
        print(f"  ROC-AUC:    {metrics['roc_auc']:.4f}")
        
        # Feature importance (if available)
        if hasattr(self.classifier, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': self.classifier.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n🔝 Top 5 Important Features:")
            for idx, row in feature_importance.head(5).iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
            
            metrics['feature_importance'] = feature_importance.to_dict('records')
        
        print()
        return self.classifier, metrics
    
    def train_regressor(self, X, y, test_size=0.2):
        """
        Train wait time prediction regressor
        
        Args:
            X: Feature matrix
            y: Target values (wait times)
            test_size: Test set proportion
        
        Returns:
            Trained model and metrics
        """
        print("\n" + "="*60)
        print("⏱️  TRAINING WAIT TIME PREDICTOR")
        print("="*60 + "\n")
        
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.linear_model import Ridge
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"Training set: {len(X_train):,} samples")
        print(f"Test set: {len(X_test):,} samples")
        print(f"Target range: {y_train.min():.1f} - {y_train.max():.1f} minutes\n")
        
        # Scale features
        self.scaler_reg = StandardScaler()
        X_train_scaled = self.scaler_reg.fit_transform(X_train)
        X_test_scaled = self.scaler_reg.transform(X_test)
        
        # Train Random Forest Regressor
        print("🔄 Training Random Forest Regressor...")
        self.regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.regressor.fit(X_train_scaled, y_train)
        print("✅ Random Forest Regressor training complete\n")
        
        # Evaluate
        y_pred = self.regressor.predict(X_test_scaled)
        
        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = np.mean(np.abs(y_test - y_pred))
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            'model_type': 'RandomForestRegressor',
            'rmse': rmse,
            'mae': mae,
            'r2_score': r2,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'features': X.shape[1],
            'timestamp': datetime.now().isoformat()
        }
        
        self.metrics['regressor'] = metrics
        
        # Print results
        print("📊 REGRESSION RESULTS:")
        print(f"  Model Type: {metrics['model_type']}")
        print(f"  RMSE:       {metrics['rmse']:.2f} minutes")
        print(f"  MAE:        {metrics['mae']:.2f} minutes")
        print(f"  R² Score:   {metrics['r2_score']:.4f}")
        
        print()
        return self.regressor, metrics
    
    def save_models(self):
        """Save trained models and scalers"""
        print("💾 Saving models...")
        
        if self.classifier:
            joblib.dump(self.classifier, f'{self.model_dir}/classifier.pkl')
            print(f"  ✅ Classifier saved ({self.model_type_used})")
        
        if self.regressor:
            joblib.dump(self.regressor, f'{self.model_dir}/regressor.pkl')
            print("  ✅ Regressor saved")
        
        if self.scaler_class:
            joblib.dump(self.scaler_class, f'{self.model_dir}/scaler_classifier.pkl')
            print("  ✅ Classification scaler saved")
        
        if self.scaler_reg:
            joblib.dump(self.scaler_reg, f'{self.model_dir}/scaler_regressor.pkl')
            print("  ✅ Regression scaler saved")
        
        # Save metrics
        with open(f'{self.model_dir}/metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print("  ✅ Metrics saved\n")
    
    def load_models(self):
        """Load trained models"""
        print("📂 Loading models...")
        
        try:
            self.classifier = joblib.load(f'{self.model_dir}/classifier.pkl')
            self.scaler_class = joblib.load(f'{self.model_dir}/scaler_classifier.pkl')
            print("  ✅ Classifier loaded")
        except:
            print("  ⚠️  Classifier not found")
        
        try:
            self.regressor = joblib.load(f'{self.model_dir}/regressor.pkl')
            self.scaler_reg = joblib.load(f'{self.model_dir}/scaler_regressor.pkl')
            print("  ✅ Regressor loaded")
        except:
            print("  ⚠️  Regressor not found")
        
        try:
            with open(f'{self.model_dir}/metrics.json', 'r') as f:
                self.metrics = json.load(f)
            print("  ✅ Metrics loaded\n")
        except:
            print("  ⚠️  Metrics not found\n")


if __name__ == '__main__':
    from features import FeatureEngineer
    from data_loader import DataLoader
    
    # Load data
    loader = DataLoader(data_dir='backend/data/processed')
    patients, visits, admissions = loader.load_all()
    
    # Engineer features
    engineer = FeatureEngineer()
    df_ml = engineer.create_ml_dataset(patients, visits)
    
    # Train classifier
    X_class, y_class, df_class = engineer.prepare_classification_features(df_ml)
    trainer = ModelTrainer()
    trainer.train_classifier(X_class, y_class, use_tabpfn=True)
    
    # Train regressor
    X_reg, y_reg, df_reg = engineer.prepare_regression_features(visits)
    trainer.train_regressor(X_reg, y_reg)
    
    # Save models
    trainer.save_models()
