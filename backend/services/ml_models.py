"""
Machine Learning models service for breast cancer classification.

Implements 4 classification models:
- Neural Network (Deep Learning)
- Random Forest (Ensemble)
- Support Vector Machine (SVM)
- Logistic Regression (Baseline)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


class MLModelsService:
    """
    Service for training and evaluating machine learning models.
    
    Handles data preprocessing, model training, evaluation, and comparison
    for breast cancer classification.
    """
    
    def __init__(self):
        """Initialize the ML models service."""
        self.models = {}
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.feature_means = None  # Store mean values for imputation
        
    def prepare_data(self, df: pd.DataFrame, target_column: str = 'cancer') -> Dict[str, Any]:
        """
        Prepare data for machine learning.

        Args:
            df: DataFrame with features and target.
            target_column: Name of the target column.

        Returns:
            dict: Preparation summary.
        """
        try:
            import logging
            logger = logging.getLogger(__name__)

            # Check if target column exists
            if target_column not in df.columns:
                return {
                    "success": False,
                    "error": f"Target column '{target_column}' not found in dataset"
                }

            # Make a copy to avoid modifying original
            df = df.copy()

            # Separate features and target
            X = df.drop(columns=[target_column])
            y = df[target_column]

            # Convert target to binary (0/1)
            # Assuming 'Yes' = 1 (cancer), 'No' = 0 (no cancer)
            y = y.map({'Yes': 1, 'No': 0})

            # Handle missing values in target
            if y.isnull().any():
                return {
                    "success": False,
                    "error": "Target column contains missing values"
                }

            # Convert specific columns to numeric (handle "No" as 0)
            columns_to_convert = ['menopause', 'agefirst', 'children', 'exercise']
            for col in columns_to_convert:
                if col in X.columns:
                    # Replace "No" with 0, then convert to numeric
                    X[col] = X[col].replace({'No': '0', 'no': '0', 'NO': '0'})
                    X[col] = pd.to_numeric(X[col], errors='coerce')
                    logger.info(f"Converted {col} to numeric. Unique values: {X[col].unique()[:10]}")

            # Select only numeric features
            numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()

            # Remove irrelevant features (id, year)
            irrelevant_features = ['id', 'year']
            numeric_features = [f for f in numeric_features if f not in irrelevant_features]

            logger.info(f"Features selected for ML: {numeric_features}")

            X = X[numeric_features]

            # Handle missing values in features (impute with mean)
            X = X.fillna(X.mean())

            # Store feature names and means for later imputation
            self.feature_names = numeric_features
            self.feature_means = X.mean().to_dict()

            logger.info(f"Feature means for imputation: {self.feature_means}")

            # Split data (80% train, 20% test)
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Scale features
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            
            return {
                "success": True,
                "n_samples": len(df),
                "n_features": len(numeric_features),
                "n_train": len(self.X_train),
                "n_test": len(self.X_test),
                "features": numeric_features,
                "class_distribution": {
                    "train": {
                        "positive": int(self.y_train.sum()),
                        "negative": int(len(self.y_train) - self.y_train.sum())
                    },
                    "test": {
                        "positive": int(self.y_test.sum()),
                        "negative": int(len(self.y_test) - self.y_test.sum())
                    }
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def train_neural_network(self) -> Dict[str, Any]:
        """
        Train a Neural Network classifier.
        
        Returns:
            dict: Training results and metrics.
        """
        try:
            # Create model
            model = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
            
            # Train model
            model.fit(self.X_train, self.y_train)
            
            # Evaluate
            metrics = self._evaluate_model(model, 'neural_network')
            
            # Store model
            self.models['neural_network'] = model
            
            return metrics

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def train_random_forest(self) -> Dict[str, Any]:
        """
        Train a Random Forest classifier.

        Returns:
            dict: Training results and metrics.
        """
        try:
            # Create model
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )

            # Train model
            model.fit(self.X_train, self.y_train)

            # Evaluate
            metrics = self._evaluate_model(model, 'random_forest')

            # Add feature importance
            metrics['feature_importance'] = {
                feature: float(importance)
                for feature, importance in zip(self.feature_names, model.feature_importances_)
            }

            # Store model
            self.models['random_forest'] = model

            return metrics

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def train_svm(self) -> Dict[str, Any]:
        """
        Train a Support Vector Machine classifier.

        Returns:
            dict: Training results and metrics.
        """
        try:
            # Create model
            model = SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                probability=True,
                random_state=42
            )

            # Train model
            model.fit(self.X_train, self.y_train)

            # Evaluate
            metrics = self._evaluate_model(model, 'svm')

            # Store model
            self.models['svm'] = model

            return metrics

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def train_logistic_regression(self) -> Dict[str, Any]:
        """
        Train a Logistic Regression classifier.

        Returns:
            dict: Training results and metrics.
        """
        try:
            # Create model
            model = LogisticRegression(
                penalty='l2',
                C=1.0,
                solver='lbfgs',
                max_iter=1000,
                random_state=42
            )

            # Train model
            model.fit(self.X_train, self.y_train)

            # Evaluate
            metrics = self._evaluate_model(model, 'logistic_regression')

            # Add coefficients
            metrics['coefficients'] = {
                feature: float(coef)
                for feature, coef in zip(self.feature_names, model.coef_[0])
            }

            # Store model
            self.models['logistic_regression'] = model

            return metrics

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _evaluate_model(self, model, model_name: str) -> Dict[str, Any]:
        """
        Evaluate a trained model.

        Args:
            model: Trained sklearn model.
            model_name: Name of the model.

        Returns:
            dict: Evaluation metrics.
        """
        # Predictions
        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)

        # Probabilities (for ROC-AUC)
        if hasattr(model, 'predict_proba'):
            y_proba_test = model.predict_proba(self.X_test)[:, 1]
        else:
            y_proba_test = model.decision_function(self.X_test)

        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(self.y_test, y_proba_test)

        # Feature importance (if available)
        feature_importance = None
        if hasattr(model, 'feature_importances_'):
            # Random Forest
            feature_importance = model.feature_importances_.tolist()
        elif hasattr(model, 'coef_'):
            # Logistic Regression, SVM
            feature_importance = np.abs(model.coef_[0]).tolist()

        # Helper function to replace inf/nan with 0
        def safe_float(value):
            if np.isnan(value) or np.isinf(value):
                return 0.0
            return float(value)

        # Calculate metrics
        metrics = {
            "success": True,
            "model_name": model_name,
            "train_metrics": {
                "accuracy": safe_float(accuracy_score(self.y_train, y_pred_train)),
                "precision": safe_float(precision_score(self.y_train, y_pred_train, zero_division=0)),
                "recall": safe_float(recall_score(self.y_train, y_pred_train, zero_division=0)),
                "f1_score": safe_float(f1_score(self.y_train, y_pred_train, zero_division=0))
            },
            "test_metrics": {
                "accuracy": safe_float(accuracy_score(self.y_test, y_pred_test)),
                "precision": safe_float(precision_score(self.y_test, y_pred_test, zero_division=0)),
                "recall": safe_float(recall_score(self.y_test, y_pred_test, zero_division=0)),
                "f1_score": safe_float(f1_score(self.y_test, y_pred_test, zero_division=0)),
                "roc_auc": safe_float(roc_auc_score(self.y_test, y_proba_test))
            },
            "confusion_matrix": {
                "train": confusion_matrix(self.y_train, y_pred_train).tolist(),
                "test": confusion_matrix(self.y_test, y_pred_test).tolist()
            },
            "roc_curve": {
                "fpr": [safe_float(x) for x in fpr],
                "tpr": [safe_float(x) for x in tpr],
                "thresholds": [safe_float(x) for x in thresholds]
            },
            "feature_importance": [safe_float(x) for x in feature_importance] if feature_importance else None,
            "feature_names": self.feature_names if hasattr(self, 'feature_names') else None
        }

        return metrics

    def train_all_models(self) -> Dict[str, Any]:
        """
        Train all 4 models.

        Returns:
            dict: Results for all models.
        """
        results = {}

        # Train Neural Network
        results['neural_network'] = self.train_neural_network()

        # Train Random Forest
        results['random_forest'] = self.train_random_forest()

        # Train SVM
        results['svm'] = self.train_svm()

        # Train Logistic Regression
        results['logistic_regression'] = self.train_logistic_regression()

        return results

    def get_best_model(self) -> Dict[str, Any]:
        """
        Get the best performing model based on F1-score.

        Returns:
            dict: Best model information.
        """
        if not self.models:
            return {
                "success": False,
                "error": "No models trained yet"
            }

        # Compare models by test F1-score
        best_model_name = None
        best_f1 = 0

        for model_name in self.models.keys():
            # Get metrics (would need to store them)
            pass

        return {
            "success": True,
            "best_model": best_model_name
        }

    def predict_single(self, input_data: Dict[str, Any], model_name: str = 'random_forest') -> Dict[str, Any]:
        """
        Predict cancer probability for a single patient.

        Args:
            input_data: Dictionary with patient features.
            model_name: Name of the model to use for prediction.

        Returns:
            dict: Prediction results with probability and risk level.
        """
        try:
            import logging
            logger = logging.getLogger(__name__)

            # Check if model exists
            if model_name not in self.models:
                return {
                    "success": False,
                    "error": f"Model '{model_name}' not trained yet. Please train models first."
                }

            # Check if scaler is fitted
            if not hasattr(self.scaler, 'mean_'):
                return {
                    "success": False,
                    "error": "Scaler not fitted. Please prepare data and train models first."
                }

            # Select only the features used in training
            if self.feature_names is None:
                return {
                    "success": False,
                    "error": "Feature names not available. Please train models first."
                }

            logger.info(f"PREDICTION DEBUG - Input data received: {input_data}")
            logger.info(f"PREDICTION DEBUG - Feature names expected: {self.feature_names}")

            # Create DataFrame with input data - only with features that exist in training
            filtered_input = {k: v for k, v in input_data.items() if k in self.feature_names}
            logger.info(f"PREDICTION DEBUG - Filtered input (matching features): {filtered_input}")

            # Create DataFrame
            input_df = pd.DataFrame([filtered_input])
            logger.info(f"PREDICTION DEBUG - DataFrame columns: {input_df.columns.tolist()}")
            logger.info(f"PREDICTION DEBUG - DataFrame values: {input_df.values}")

            # Ensure all required features are present
            missing_features = set(self.feature_names) - set(input_df.columns)
            if missing_features:
                logger.warning(f"PREDICTION DEBUG - Missing features (will be imputed with mean): {missing_features}")
                # Fill missing features with mean from training data
                for feature in missing_features:
                    if self.feature_means and feature in self.feature_means:
                        input_df[feature] = self.feature_means[feature]
                        logger.info(f"PREDICTION DEBUG - Filled {feature} with mean: {self.feature_means[feature]}")
                    else:
                        input_df[feature] = 0
                        logger.warning(f"PREDICTION DEBUG - No mean available for {feature}, using 0")

            # Select and order features to match training
            input_df = input_df[self.feature_names]
            logger.info(f"PREDICTION DEBUG - Final DataFrame before scaling:\n{input_df}")
            logger.info(f"PREDICTION DEBUG - Final values: {input_df.values[0]}")

            # Handle missing values (impute with mean from training)
            for col in input_df.columns:
                if input_df[col].isnull().any():
                    if self.feature_means and col in self.feature_means:
                        input_df[col] = input_df[col].fillna(self.feature_means[col])
                    else:
                        input_df[col] = input_df[col].fillna(0)

            # Scale features
            input_scaled = self.scaler.transform(input_df)
            logger.info(f"PREDICTION DEBUG - Scaled values: {input_scaled[0]}")

            # Get model
            model = self.models[model_name]

            # Make prediction
            prediction = model.predict(input_scaled)[0]
            logger.info(f"PREDICTION DEBUG - Raw prediction: {prediction}")

            # Get probability if available
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(input_scaled)[0]
                logger.info(f"PREDICTION DEBUG - Probabilities [No Cancer, Cancer]: {probabilities}")
                probability_cancer = float(probabilities[1])  # Probability of class 1 (cancer)
            else:
                # For SVM without probability
                probability_cancer = float(prediction)
                logger.info(f"PREDICTION DEBUG - SVM prediction (no proba): {probability_cancer}")

            # Determine risk level
            if probability_cancer < 0.3:
                risk_level = "Bajo"
                risk_color = "green"
            elif probability_cancer < 0.6:
                risk_level = "Moderado"
                risk_color = "orange"  # Changed from yellow to orange for better visibility
            else:
                risk_level = "Alto"
                risk_color = "red"

            logger.info(f"PREDICTION DEBUG - Final probability: {probability_cancer}, Risk: {risk_level}")

            return {
                "success": True,
                "prediction": int(prediction),
                "probability": probability_cancer,
                "probability_percentage": round(probability_cancer * 100, 2),
                "risk_level": risk_level,
                "risk_color": risk_color,
                "model_used": model_name,
                "interpretation": self._get_interpretation(probability_cancer, risk_level),
                "debug_info": {
                    "input_received": input_data,
                    "features_used": self.feature_names,
                    "scaled_values": input_scaled[0].tolist()
                }
            }

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"PREDICTION ERROR: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": f"Error making prediction: {str(e)}"
            }

    def _get_interpretation(self, probability: float, risk_level: str) -> str:
        """
        Generate interpretation text based on probability.

        Args:
            probability: Probability of cancer.
            risk_level: Risk level classification.

        Returns:
            str: Interpretation text.
        """
        if risk_level == "Bajo":
            return (
                "La probabilidad de cáncer de mama es baja según los factores de riesgo proporcionados. "
                "Se recomienda mantener controles médicos regulares y hábitos de vida saludables."
            )
        elif risk_level == "Moderado":
            return (
                "La probabilidad de cáncer de mama es moderada. Se recomienda consultar con un especialista "
                "para evaluación adicional y considerar estudios complementarios según criterio médico."
            )
        else:
            return (
                "La probabilidad de cáncer de mama es alta según los factores de riesgo analizados. "
                "Se recomienda consulta urgente con un especialista en mastología para evaluación "
                "detallada y estudios diagnósticos complementarios."
            )

