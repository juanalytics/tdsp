"""
Script principal de evaluación para el modelo de retención estudiantil.

Este script carga los modelos entrenados y genera reportes completos
de evaluación con visualizaciones y métricas detalladas.
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
import json
from pathlib import Path

# Añadir el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from nombre_paquete.models.baseline_model import BaselineModel
from nombre_paquete.models.neural_network import NeuralNetworkModel
from nombre_paquete.evaluation.model_evaluator import ModelEvaluator

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_evaluation_data():
    """
    Carga los datos necesarios para evaluación.
    
    Returns:
        Tuple con características y variable objetivo
    """
    logger.info("📂 Cargando datos para evaluación...")
    
    processed_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    
    # Cargar características y target
    features_path = processed_dir / "modeling_features.csv"
    target_path = processed_dir / "modeling_target.csv"
    
    if not features_path.exists() or not target_path.exists():
        raise FileNotFoundError("No se encontraron los archivos de datos para evaluación.")
    
    features_df = pd.read_csv(features_path)
    target = pd.read_csv(target_path).squeeze()
    
    logger.info(f"✅ Cargados datos con {len(features_df)} registros")
    
    return features_df, target

def load_trained_models():
    """
    Carga los modelos entrenados.
    
    Returns:
        Diccionario con modelos cargados
    """
    logger.info("🤖 Cargando modelos entrenados...")
    
    models_dir = Path(__file__).parent.parent.parent / "models"
    models = {}
    
    # Cargar modelos baseline
    baseline_models = {
        'logistic_regression': 'logistic',
        'random_forest': 'random_forest'
    }
    
    for model_name, model_type in baseline_models.items():
        model_path = models_dir / f"{model_name}_model.pkl"
        if model_path.exists():
            model = BaselineModel(model_type=model_type)
            model.load_model(str(model_path))
            models[model_name] = model
            logger.info(f"✅ Cargado {model_name}")
        else:
            logger.warning(f"⚠️ No se encontró {model_name}")
    
    # Cargar modelo de red neuronal
    nn_path = models_dir / "neural_network_model.pkl"
    if nn_path.exists():
        nn_model = NeuralNetworkModel(input_dim=0)  # Se actualizará al cargar
        nn_model.load_model(str(nn_path))
        models['neural_network'] = nn_model
        logger.info("✅ Cargado neural_network")
    else:
        logger.warning("⚠️ No se encontró neural_network_model.pkl")
    
    return models

def generate_comprehensive_evaluation(features_df, target, models):
    """
    Genera evaluación completa de todos los modelos.
    
    Args:
        features_df: DataFrame con características
        target: Series con variable objetivo
        models: Diccionario con modelos cargados
        
    Returns:
        Diccionario con resultados de evaluación
    """
    logger.info("📊 Generando evaluación completa...")
    
    evaluator = ModelEvaluator()
    evaluation_results = {}
    
    # Evaluar cada modelo
    for model_name, model in models.items():
        logger.info(f"📋 Evaluando {model_name}...")
        
        # Hacer predicciones
        y_pred = model.predict(features_df)
        y_pred_proba = model.predict_proba(features_df)
        
        # Ajustar formato de probabilidades para modelos baseline
        if hasattr(model, 'model_type') and model.model_type in ['logistic', 'random_forest']:
            if len(y_pred_proba.shape) > 1:
                y_pred_proba = y_pred_proba[:, 1]
        
        # Obtener importancia de características si está disponible
        feature_importance = None
        if hasattr(model, 'get_feature_importance'):
            try:
                feature_importance = model.get_feature_importance(features_df.columns.tolist())
            except:
                pass
        
        # Generar reporte de evaluación
        plots_dir = Path(__file__).parent.parent.parent / "docs" / "modeling" / "plots"
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        evaluation_report = evaluator.generate_evaluation_report(
            y_true=target.values,
            y_pred=y_pred,
            y_pred_proba=y_pred_proba,
            model_name=model_name,
            feature_importance=feature_importance,
            save_dir=str(plots_dir)
        )
        
        evaluation_results[model_name] = evaluation_report
        
        # Mostrar métricas principales
        metrics = evaluation_report['metrics']
        logger.info(f"   F1-Score: {metrics['f1_score']:.3f}")
        logger.info(f"   ROC-AUC: {metrics['roc_auc']:.3f}")
        logger.info(f"   Accuracy: {metrics['accuracy']:.3f}")
    
    return evaluation_results

def create_final_comparison_report(evaluation_results):
    """
    Crea reporte final de comparación de modelos.
    
    Args:
        evaluation_results: Resultados de evaluación
        
    Returns:
        DataFrame con comparación final
    """
    logger.info("🏆 Creando reporte final de comparación...")
    
    evaluator = ModelEvaluator()
    comparison_df = evaluator.compare_models(evaluation_results)
    
    # Guardar comparación
    output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    comparison_path = output_dir / "final_model_comparison.csv"
    comparison_df.to_csv(comparison_path, index=False)
    
    # Crear gráfico de comparación
    plots_dir = Path(__file__).parent.parent.parent / "docs" / "modeling" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    # Preparar métricas para el gráfico
    models_metrics = {}
    for model_name, results in evaluation_results.items():
        models_metrics[model_name] = results['metrics']
    
    comparison_plot_path = plots_dir / "final_model_comparison.png"
    evaluator.create_metrics_comparison_plot(models_metrics, str(comparison_plot_path))
    
    logger.info(f"✅ Comparación final guardada en {comparison_path}")
    logger.info("🏆 Ranking final de modelos:")
    for i, row in comparison_df.iterrows():
        logger.info(f"   {i+1}. {row['Modelo']}: F1={row['F1-Score']:.3f}, ROC-AUC={row['ROC-AUC']:.3f}")
    
    return comparison_df

def generate_evaluation_summary(evaluation_results, comparison_df):
    """
    Genera un resumen ejecutivo de la evaluación.
    
    Args:
        evaluation_results: Resultados de evaluación
        comparison_df: DataFrame de comparación
        
    Returns:
        Diccionario con resumen ejecutivo
    """
    logger.info("📋 Generando resumen ejecutivo...")
    
    # Encontrar el mejor modelo
    best_model = comparison_df.iloc[0]
    
    # Crear resumen
    summary = {
        'total_models_evaluated': len(evaluation_results),
        'best_model': {
            'name': best_model['Modelo'],
            'f1_score': best_model['F1-Score'],
            'roc_auc': best_model['ROC-AUC'],
            'accuracy': best_model['Accuracy'],
            'precision': best_model['Precision'],
            'recall': best_model['Recall']
        },
        'all_models_performance': comparison_df.to_dict('records'),
        'evaluation_date': pd.Timestamp.now().isoformat()
    }
    
    # Guardar resumen
    output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    summary_path = output_dir / "evaluation_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info(f"✅ Resumen ejecutivo guardado en {summary_path}")
    logger.info(f"🏆 Mejor modelo: {best_model['Modelo']} (F1: {best_model['F1-Score']:.3f})")
    
    return summary

def save_evaluation_results(evaluation_results, comparison_df, summary):
    """
    Guarda todos los resultados de evaluación.
    
    Args:
        evaluation_results: Resultados de evaluación
        comparison_df: DataFrame de comparación
        summary: Resumen ejecutivo
    """
    logger.info("💾 Guardando resultados de evaluación...")
    
    # Crear directorio de resultados
    results_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar resultados completos
    evaluation_results_complete = {
        'evaluation_results': evaluation_results,
        'model_comparison': comparison_df.to_dict('records'),
        'executive_summary': summary,
        'evaluation_metadata': {
            'total_models': len(evaluation_results),
            'evaluation_date': pd.Timestamp.now().isoformat(),
            'best_model': summary['best_model']['name']
        }
    }
    
    results_path = results_dir / "evaluation_results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results_complete, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info(f"✅ Resultados completos guardados en {results_path}")

def main():
    """
    Función principal del script de evaluación.
    """
    logger.info("🚀 Iniciando evaluación de modelos...")
    
    try:
        # Cargar datos
        features_df, target = load_evaluation_data()
        
        # Cargar modelos entrenados
        models = load_trained_models()
        
        if not models:
            raise ValueError("No se encontraron modelos entrenados para evaluar")
        
        # Generar evaluación completa
        evaluation_results = generate_comprehensive_evaluation(features_df, target, models)
        
        # Crear comparación final
        comparison_df = create_final_comparison_report(evaluation_results)
        
        # Generar resumen ejecutivo
        summary = generate_evaluation_summary(evaluation_results, comparison_df)
        
        # Guardar resultados
        save_evaluation_results(evaluation_results, comparison_df, summary)
        
        logger.info("✅ Evaluación completada exitosamente")
        
        return evaluation_results, comparison_df, summary
        
    except Exception as e:
        logger.error(f"❌ Error en evaluación: {e}")
        raise

if __name__ == "__main__":
    main()
