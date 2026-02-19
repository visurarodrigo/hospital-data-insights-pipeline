"""
Model Evaluation Module
Comprehensive evaluation and visualization of model performance
"""

import pandas as pd
import numpy as np
import json
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, precision_recall_curve
)
import joblib


class ModelEvaluator:
    """Evaluates and analyzes model performance"""
    
    def __init__(self, model_dir='backend/models'):
        """
        Initialize evaluator
        
        Args:
            model_dir: Directory containing trained models
        """
        self.model_dir = model_dir
        self.load_metrics()
    
    def load_metrics(self):
        """Load saved metrics"""
        try:
            with open(f'{self.model_dir}/metrics.json', 'r') as f:
                self.metrics = json.load(f)
            print("✅ Metrics loaded")
        except:
            self.metrics = {}
            print("⚠️  No metrics found")
    
    def generate_classification_report(self, y_true, y_pred, y_pred_proba=None):
        """
        Generate detailed classification report
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities (optional)
        
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n" + "="*60)
        print("📊 CLASSIFICATION EVALUATION REPORT")
        print("="*60 + "\n")
        
        # Classification report
        print("Detailed Metrics:")
        print(classification_report(y_true, y_pred, target_names=['Low Risk', 'High Risk']))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        print("\nConfusion Matrix:")
        print(f"                Predicted Low    Predicted High")
        print(f"Actual Low      {cm[0][0]:^15}  {cm[0][1]:^15}")
        print(f"Actual High     {cm[1][0]:^15}  {cm[1][1]:^15}")
        
        # Calculate additional metrics
        tn, fp, fn, tp = cm.ravel()
        
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0
        
        print(f"\nAdditional Metrics:")
        print(f"  Specificity (TNR): {specificity:.4f}")
        print(f"  Negative Predictive Value: {npv:.4f}")
        print(f"  False Positive Rate: {fp / (fp + tn):.4f}")
        print(f"  False Negative Rate: {fn / (fn + tp):.4f}")
        
        report = {
            'confusion_matrix': cm.tolist(),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp),
            'specificity': float(specificity),
            'npv': float(npv)
        }
        
        return report
    
    def generate_regression_report(self, y_true, y_pred):
        """
        Generate detailed regression report
        
        Args:
            y_true: True values
            y_pred: Predicted values
        
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n" + "="*60)
        print("📊 REGRESSION EVALUATION REPORT")
        print("="*60 + "\n")
        
        errors = y_true - y_pred
        abs_errors = np.abs(errors)
        
        print("Error Statistics:")
        print(f"  Mean Absolute Error: {np.mean(abs_errors):.2f}")
        print(f"  Median Absolute Error: {np.median(abs_errors):.2f}")
        print(f"  Max Error: {np.max(abs_errors):.2f}")
        print(f"  Min Error: {np.min(abs_errors):.2f}")
        print(f"  Std Dev of Errors: {np.std(errors):.2f}")
        
        # Percentage within thresholds
        within_5min = (abs_errors <= 5).mean() * 100
        within_10min = (abs_errors <= 10).mean() * 100
        within_15min = (abs_errors <= 15).mean() * 100
        
        print(f"\nPrediction Accuracy:")
        print(f"  Within 5 minutes:  {within_5min:.1f}%")
        print(f"  Within 10 minutes: {within_10min:.1f}%")
        print(f"  Within 15 minutes: {within_15min:.1f}%")
        
        report = {
            'mae': float(np.mean(abs_errors)),
            'median_ae': float(np.median(abs_errors)),
            'max_error': float(np.max(abs_errors)),
            'std_error': float(np.std(errors)),
            'within_5min_pct': float(within_5min),
            'within_10min_pct': float(within_10min),
            'within_15min_pct': float(within_15min)
        }
        
        return report
    
    def display_metrics_summary(self):
        """Display summary of all model metrics"""
        print("\n" + "="*60)
        print("📈 MODEL PERFORMANCE SUMMARY")
        print("="*60 + "\n")
        
        if 'classifier' in self.metrics:
            print("🎯 Classification Model:")
            clf_metrics = self.metrics['classifier']
            print(f"  Model Type: {clf_metrics.get('model_type', 'Unknown')}")
            print(f"  Accuracy:   {clf_metrics.get('accuracy', 0):.4f}")
            print(f"  ROC-AUC:    {clf_metrics.get('roc_auc', 0):.4f}")
            print(f"  F1 Score:   {clf_metrics.get('f1_score', 0):.4f}")
            print(f"  Training Date: {clf_metrics.get('timestamp', 'Unknown')[:10]}")
        
        if 'regressor' in self.metrics:
            print("\n⏱️  Regression Model:")
            reg_metrics = self.metrics['regressor']
            print(f"  Model Type: {reg_metrics.get('model_type', 'Unknown')}")
            print(f"  RMSE:       {reg_metrics.get('rmse', 0):.2f} minutes")
            print(f"  R² Score:   {reg_metrics.get('r2_score', 0):.4f}")
            print(f"  Training Date: {reg_metrics.get('timestamp', 'Unknown')[:10]}")
        
        print()
    
    def export_evaluation_report(self, output_path='backend/models/evaluation_report.json'):
        """Export complete evaluation report"""
        report = {
            'summary': self.metrics,
            'generated_at': pd.Timestamp.now().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Evaluation report saved to {output_path}")


if __name__ == '__main__':
    evaluator = ModelEvaluator()
    evaluator.display_metrics_summary()
    evaluator.export_evaluation_report()
