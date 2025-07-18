"""
Módulo de evaluación de modelos para predicción de retención estudiantil.

Este módulo contiene funciones para evaluar el rendimiento de los modelos
de predicción de abandono estudiantil con métricas y visualizaciones.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    f1_score, precision_score, recall_score, accuracy_score,
    roc_curve, precision_recall_curve, average_precision_score
)
import logging
from typing import Dict, Any, Tuple, Optional
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """
    Clase para evaluar modelos de predicción de retención estudiantil.
    """
    
    def __init__(self):
        """Inicializa el evaluador de modelos."""
        self.metrics = {}
        self.plots_dir = None
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray) -> Dict[str, float]:
        """
        Calcula métricas de evaluación del modelo.
        
        Args:
            y_true: Valores reales
            y_pred: Predicciones binarias
            y_pred_proba: Probabilidades de predicción
            
        Returns:
            Diccionario con métricas de evaluación
        """
        logger.info("📊 Calculando métricas de evaluación...")
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_pred_proba),
            'average_precision': average_precision_score(y_true, y_pred_proba)
        }
        
        logger.info(f"✅ Métricas calculadas - F1: {metrics['f1_score']:.3f}, ROC-AUC: {metrics['roc_auc']:.3f}")
        return metrics
    
    def create_confusion_matrix_plot(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                   save_path: Optional[str] = None) -> plt.Figure:
        """
        Crea gráfico de matriz de confusión.
        
        Args:
            y_true: Valores reales
            y_pred: Predicciones
            save_path: Ruta para guardar el gráfico
            
        Returns:
            Figura de matplotlib
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Abandono', 'Abandono'],
                   yticklabels=['No Abandono', 'Abandono'])
        plt.title('Matriz de Confusión')
        plt.ylabel('Valor Real')
        plt.xlabel('Predicción')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Matriz de confusión guardada en {save_path}")
        
        return plt.gcf()
    
    def create_roc_curve_plot(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Crea gráfico de curva ROC.
        
        Args:
            y_true: Valores reales
            y_pred_proba: Probabilidades de predicción
            save_path: Ruta para guardar el gráfico
            
        Returns:
            Figura de matplotlib
        """
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        auc = roc_auc_score(y_true, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Curva ROC')
        plt.legend(loc="lower right")
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Curva ROC guardada en {save_path}")
        
        return plt.gcf()
    
    def create_precision_recall_curve_plot(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                                         save_path: Optional[str] = None) -> plt.Figure:
        """
        Crea gráfico de curva Precision-Recall.
        
        Args:
            y_true: Valores reales
            y_pred_proba: Probabilidades de predicción
            save_path: Ruta para guardar el gráfico
            
        Returns:
            Figura de matplotlib
        """
        precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
        ap = average_precision_score(y_true, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='darkorange', lw=2, label=f'PR curve (AP = {ap:.3f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Curva Precision-Recall')
        plt.legend(loc="lower left")
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Curva Precision-Recall guardada en {save_path}")
        
        return plt.gcf()
    
    def create_feature_importance_plot(self, feature_importance: pd.DataFrame, 
                                     top_n: int = 20, save_path: Optional[str] = None) -> plt.Figure:
        """
        Crea gráfico de importancia de características.
        
        Args:
            feature_importance: DataFrame con importancia de características
            top_n: Número de características principales a mostrar
            save_path: Ruta para guardar el gráfico
            
        Returns:
            Figura de matplotlib
        """
        if feature_importance.empty:
            logger.warning("No hay datos de importancia de características")
            return plt.figure()
        
        # Tomar las top_n características
        top_features = feature_importance.head(top_n)
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importancia')
        plt.title(f'Top {top_n} Características Más Importantes')
        plt.gca().invert_yaxis()
        
        # Añadir valores en las barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{width:.3f}', ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Gráfico de importancia guardado en {save_path}")
        
        return plt.gcf()
    
    def create_metrics_comparison_plot(self, models_metrics: Dict[str, Dict[str, float]],
                                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Crea gráfico de comparación de métricas entre modelos.
        
        Args:
            models_metrics: Diccionario con métricas de diferentes modelos
            save_path: Ruta para guardar el gráfico
            
        Returns:
            Figura de matplotlib
        """
        # Preparar datos para el gráfico
        metrics_df = pd.DataFrame(models_metrics).T
        
        # Crear gráfico de barras
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
        titles = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        
        for i, (metric, title) in enumerate(zip(metrics_to_plot, titles)):
            row, col = i // 2, i % 2
            if metric in metrics_df.columns:
                axes[row, col].bar(metrics_df.index, metrics_df[metric])
                axes[row, col].set_title(title)
                axes[row, col].set_ylabel(metric.capitalize())
                axes[row, col].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✅ Comparación de modelos guardada en {save_path}")
        
        return fig
    
    def generate_evaluation_report(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                 y_pred_proba: np.ndarray, model_name: str,
                                 feature_importance: Optional[pd.DataFrame] = None,
                                 save_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Genera un reporte completo de evaluación del modelo.
        
        Args:
            y_true: Valores reales
            y_pred: Predicciones binarias
            y_pred_proba: Probabilidades de predicción
            model_name: Nombre del modelo
            feature_importance: DataFrame con importancia de características
            save_dir: Directorio para guardar gráficos
            
        Returns:
            Diccionario con reporte completo
        """
        logger.info(f"📋 Generando reporte de evaluación para {model_name}...")
        
        # Calcular métricas
        metrics = self.calculate_metrics(y_true, y_pred, y_pred_proba)
        
        # Generar reporte de clasificación
        classification_rep = classification_report(y_true, y_pred, output_dict=True)
        
        # Crear gráficos
        plots = {}
        
        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            
            # Matriz de confusión
            cm_path = f"{save_dir}/{model_name}_confusion_matrix.png"
            self.create_confusion_matrix_plot(y_true, y_pred, cm_path)
            plots['confusion_matrix'] = cm_path
            
            # Curva ROC
            roc_path = f"{save_dir}/{model_name}_roc_curve.png"
            self.create_roc_curve_plot(y_true, y_pred_proba, roc_path)
            plots['roc_curve'] = roc_path
            
            # Curva Precision-Recall
            pr_path = f"{save_dir}/{model_name}_precision_recall_curve.png"
            self.create_precision_recall_curve_plot(y_true, y_pred_proba, pr_path)
            plots['precision_recall_curve'] = pr_path
            
            # Importancia de características
            if feature_importance is not None and not feature_importance.empty:
                fi_path = f"{save_dir}/{model_name}_feature_importance.png"
                self.create_feature_importance_plot(feature_importance, save_path=fi_path)
                plots['feature_importance'] = fi_path
        
        # Crear reporte completo
        report = {
            'model_name': model_name,
            'metrics': metrics,
            'classification_report': classification_rep,
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'plots': plots
        }
        
        logger.info(f"✅ Reporte de evaluación completado para {model_name}")
        return report
    
    def save_evaluation_report(self, report: Dict[str, Any], filepath: str):
        """
        Guarda el reporte de evaluación en formato JSON.
        
        Args:
            report: Reporte de evaluación
            filepath: Ruta donde guardar el reporte
        """
        import json
        
        # Crear directorio si no existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar reporte
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Reporte de evaluación guardado en {filepath}")
    
    def compare_models(self, models_results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Compara múltiples modelos y genera un DataFrame de comparación.
        
        Args:
            models_results: Diccionario con resultados de diferentes modelos
            
        Returns:
            DataFrame con comparación de modelos
        """
        logger.info("🔍 Comparando modelos...")
        
        comparison_data = []
        
        for model_name, results in models_results.items():
            if 'metrics' in results:
                metrics = results['metrics']
                comparison_data.append({
                    'Modelo': model_name,
                    'Accuracy': metrics.get('accuracy', 0),
                    'Precision': metrics.get('precision', 0),
                    'Recall': metrics.get('recall', 0),
                    'F1-Score': metrics.get('f1_score', 0),
                    'ROC-AUC': metrics.get('roc_auc', 0),
                    'Average Precision': metrics.get('average_precision', 0)
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('F1-Score', ascending=False)
        
        logger.info(f"✅ Comparación completada para {len(comparison_df)} modelos")
        return comparison_df 