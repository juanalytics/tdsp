"""
Módulo del modelo baseline para predicción de retención estudiantil.

Este módulo contiene implementaciones de modelos simples para establecer
una línea base de rendimiento antes de implementar modelos más complejos.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from typing import Dict, Tuple, Any, Optional
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaselineModel:
    """
    Clase para implementar modelos baseline de predicción de retención estudiantil.
    """
    
    def __init__(self, model_type: str = 'logistic'):
        """
        Inicializa el modelo baseline.
        
        Args:
            model_type: Tipo de modelo ('logistic' o 'random_forest')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_fitted = False
        
        if model_type == 'logistic':
            self.model = LogisticRegression(random_state=42, max_iter=1000)
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError("model_type debe ser 'logistic' o 'random_forest'")
    
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepara los datos para entrenamiento y validación.
        
        Args:
            X: DataFrame con características
            y: Series con variable objetivo
            test_size: Proporción para conjunto de prueba
            
        Returns:
            Tuple con datos de entrenamiento y prueba
        """
        logger.info("📊 Preparando datos para entrenamiento...")
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Escalar características numéricas
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        logger.info(f"✅ Datos preparados - Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Entrena el modelo baseline.
        
        Args:
            X: DataFrame con características
            y: Series con variable objetivo
            
        Returns:
            Diccionario con métricas de entrenamiento
        """
        logger.info(f"🚀 Entrenando modelo baseline ({self.model_type})...")
        
        # Preparar datos
        X_train, X_test, y_train, y_test = self.prepare_data(X, y)
        
        # Entrenar modelo
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Evaluar modelo
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calcular métricas
        metrics = {
            'accuracy': self.model.score(X_test, y_test),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        logger.info(f"✅ Modelo entrenado - F1: {metrics['f1_score']:.3f}, ROC-AUC: {metrics['roc_auc']:.3f}")
        return metrics
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]:
        """
        Realiza validación cruzada del modelo.
        
        Args:
            X: DataFrame con características
            y: Series con variable objetivo
            cv: Número de folds para validación cruzada
            
        Returns:
            Diccionario con métricas de validación cruzada
        """
        logger.info(f"🔄 Realizando validación cruzada ({cv} folds)...")
        
        # Escalar datos
        X_scaled = self.scaler.fit_transform(X)
        
        # Validación cruzada
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=cv, scoring='f1')
        
        metrics = {
            'cv_f1_mean': cv_scores.mean(),
            'cv_f1_std': cv_scores.std(),
            'cv_f1_scores': cv_scores.tolist()
        }
        
        logger.info(f"✅ Validación cruzada completada - F1: {metrics['cv_f1_mean']:.3f} ± {metrics['cv_f1_std']:.3f}")
        return metrics
    
    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        """
        Obtiene la importancia de características del modelo.
        
        Args:
            feature_names: Lista de nombres de características
            
        Returns:
            DataFrame con importancia de características
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe estar entrenado antes de obtener importancia de características")
        
        if self.model_type == 'random_forest':
            importance = self.model.feature_importances_
        elif self.model_type == 'logistic':
            importance = np.abs(self.model.coef_[0])
        else:
            return pd.DataFrame()
        
        # Crear DataFrame con importancia
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Realiza predicciones con el modelo entrenado.
        
        Args:
            X: DataFrame con características
            
        Returns:
            Array con predicciones
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe estar entrenado antes de hacer predicciones")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Realiza predicciones de probabilidad con el modelo entrenado.
        
        Args:
            X: DataFrame con características
            
        Returns:
            Array con probabilidades de predicción
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe estar entrenado antes de hacer predicciones")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    def save_model(self, filepath: str):
        """
        Guarda el modelo entrenado.
        
        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe estar entrenado antes de guardarlo")
        
        # Crear directorio si no existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo y scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"✅ Modelo guardado en {filepath}")
    
    def load_model(self, filepath: str):
        """
        Carga un modelo guardado.
        
        Args:
            filepath: Ruta del modelo a cargar
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.model_type = model_data['model_type']
        self.is_fitted = True
        
        logger.info(f"✅ Modelo cargado desde {filepath}")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del modelo.
        
        Returns:
            Diccionario con información del modelo
        """
        summary = {
            'model_type': self.model_type,
            'is_fitted': self.is_fitted,
            'model_params': self.model.get_params() if self.is_fitted else None
        }
        
        return summary 