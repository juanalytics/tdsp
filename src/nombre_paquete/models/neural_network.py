"""
Módulo del modelo de red neuronal para predicción de retención estudiantil.

Este módulo contiene implementaciones de redes neuronales (MLP) para
la predicción de abandono estudiantil basado en el proyecto charter.
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib
import logging
from typing import Dict, Tuple, Any, Optional, List
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeuralNetworkModel:
    """
    Clase para implementar modelo de red neuronal (MLP) para predicción de retención estudiantil.
    """
    
    def __init__(self, input_dim: int, architecture: Optional[List[int]] = None):
        """
        Inicializa el modelo de red neuronal.
        
        Args:
            input_dim: Dimensión de entrada (número de características)
            architecture: Lista con número de neuronas por capa oculta
        """
        self.input_dim = input_dim
        self.architecture = architecture if architecture is not None else [128, 64, 32]  # Arquitectura por defecto
        self.model = None
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.pipeline = None
        self.is_fitted = False
        self.history = None
        
        # Configurar TensorFlow para evitar warnings
        try:
            tf.get_logger().setLevel('ERROR')
        except:
            pass
    
    def build_model(self) -> keras.Model:
        """
        Construye la arquitectura de la red neuronal.
        
        Returns:
            Modelo de Keras compilado
        """
        logger.info(f"🏗️ Construyendo modelo MLP con arquitectura: {self.architecture}")
        
        model = keras.Sequential()
        
        # Capa de entrada
        model.add(layers.Dense(self.architecture[0], activation='relu', input_shape=(self.input_dim,)))
        model.add(layers.Dropout(0.3))
        model.add(layers.BatchNormalization())
        
        # Capas ocultas
        for units in self.architecture[1:]:
            model.add(layers.Dense(units, activation='relu'))
            model.add(layers.Dropout(0.2))
            model.add(layers.BatchNormalization())
        
        # Capa de salida
        model.add(layers.Dense(1, activation='sigmoid'))
        
        # Compilar modelo
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        logger.info(f"✅ Modelo construido con {model.count_params():,} parámetros")
        return model
    
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, val_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepara los datos para entrenamiento, validación y prueba.
        
        Args:
            X: DataFrame con características
            y: Series con variable objetivo
            test_size: Proporción para conjunto de prueba
            val_size: Proporción para conjunto de validación (del conjunto de entrenamiento)
            
        Returns:
            Tuple con datos de entrenamiento, validación y prueba
        """
        logger.info("📊 Preparando datos para entrenamiento...")
        
        # Dividir datos en train y test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Dividir train en train y validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=val_size, random_state=42, stratify=y_train
        )
        
        logger.info(f"✅ Datos preparados - Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def train(self, X: pd.DataFrame, y: pd.Series, epochs: int = 100, batch_size: int = 32, patience: int = 10) -> Dict[str, Any]:
        """
        Entrena el modelo de red neuronal.
        
        Args:
            X: DataFrame con características
            y: Series con variable objetivo
            epochs: Número máximo de épocas
            batch_size: Tamaño del batch
            patience: Paciencia para early stopping
            
        Returns:
            Diccionario con métricas de entrenamiento
        """
        logger.info("🚀 Entrenando modelo de red neuronal...")
        
        # Seleccionar solo columnas numéricas
        numeric_cols = X.select_dtypes(include=np.number).columns
        X_numeric = X[numeric_cols]
        self.input_dim = len(numeric_cols)

        # Preparar datos
        X_train, X_val, X_test, y_train, y_val, y_test = self.prepare_data(X_numeric, y)
        
        # Construir modelo de Keras
        self.model = self.build_model()

        # Crear pipeline de preprocesamiento
        preprocessor = Pipeline([
            ('imputer', self.imputer),
            ('scaler', self.scaler)
        ])

        # Procesar datos
        X_train_processed = preprocessor.fit_transform(X_train)
        X_val_processed = preprocessor.transform(X_val)
        X_test_processed = preprocessor.transform(X_test)

        # Guardar el preprocesador ajustado
        self.pipeline = preprocessor

        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=patience,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        )
        
        # Entrenar modelo
        self.history = self.model.fit(
            X_train_processed, y_train,
            validation_data=(X_val_processed, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        self.is_fitted = True
        
        # Evaluar modelo
        if self.model is not None:
            y_pred_proba = self.model.predict(X_test_processed)
            y_pred = (y_pred_proba > 0.5).astype(int)
        else:
            raise ValueError("Modelo no inicializado correctamente")
        
        # Calcular métricas
        metrics = {
            'accuracy': self.model.evaluate(X_test_processed, y_test, verbose=0)[1],
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'classification_report': classification_report(y_test, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'training_history': self.history.history
        }
        
        logger.info(f"✅ Modelo entrenado - F1: {metrics['f1_score']:.3f}, ROC-AUC: {metrics['roc_auc']:.3f}")
        return metrics
    
    def plot_training_history(self, save_path: Optional[str] = None):
        """
        Genera gráficos del historial de entrenamiento.
        
        Args:
            save_path: Ruta donde guardar los gráficos
        """
        if self.history is None:
            logger.warning("No hay historial de entrenamiento disponible")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0, 0].plot(self.history.history['loss'], label='Train Loss')
        axes[0, 0].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[0, 0].set_title('Model Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        
        # Accuracy
        axes[0, 1].plot(self.history.history['accuracy'], label='Train Accuracy')
        axes[0, 1].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0, 1].set_title('Model Accuracy')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy')
        axes[0, 1].legend()
        
        # Precision
        axes[1, 0].plot(self.history.history['precision'], label='Train Precision')
        axes[1, 0].plot(self.history.history['val_precision'], label='Validation Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        
        # Recall
        axes[1, 1].plot(self.history.history['recall'], label='Train Recall')
        axes[1, 1].plot(self.history.history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Gráficos guardados en {save_path}")
        
        plt.show()
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Realiza predicciones con el modelo entrenado.
        
        Args:
            X: DataFrame con características
            
        Returns:
            Array con predicciones binarias
        """
        if not self.is_fitted:
            raise ValueError("El modelo debe estar entrenado antes de hacer predicciones")
        
        numeric_cols = X.select_dtypes(include=np.number).columns
        X_processed = self.pipeline.transform(X[numeric_cols])
        y_pred_proba = self.model.predict(X_processed)
        return (y_pred_proba > 0.5).astype(int)
    
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
        
        numeric_cols = X.select_dtypes(include=np.number).columns
        X_processed = self.pipeline.transform(X[numeric_cols])
        return self.model.predict(X_processed)
    
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
        
        # Guardar modelo Keras y pipeline preprocesador por separado
        self.model.save(filepath.replace('.pkl', '.keras'))
        joblib.dump(self.pipeline, filepath.replace('.pkl', '_preprocessor.pkl'))
        
        logger.info(f"✅ Modelo Keras guardado en {filepath.replace('.pkl', '.keras')}")
        logger.info(f"✅ Preprocesador guardado en {filepath.replace('.pkl', '_preprocessor.pkl')}")
    
    def load_model(self, filepath: str):
        """
        Carga un modelo guardado.
        
        Args:
            filepath: Ruta del modelo a cargar
        """
        self.model = keras.models.load_model(filepath.replace('.pkl', '.keras'))
        self.pipeline = joblib.load(filepath.replace('.pkl', '_preprocessor.pkl'))
        self.scaler = self.pipeline.named_steps['scaler']
        self.imputer = self.pipeline.named_steps['imputer']
        self.is_fitted = True
        
        logger.info(f"✅ Modelo cargado desde {filepath.replace('.pkl', '.keras')}")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del modelo.
        
        Returns:
            Diccionario con información del modelo
        """
        summary = {
            'model_type': 'MLP',
            'is_fitted': self.is_fitted,
            'architecture': self.architecture,
            'input_dim': self.input_dim,
            'total_params': self.model.count_params() if self.is_fitted else None
        }
        
        return summary 