"""
Script principal de entrenamiento para el modelo de retención estudiantil.

Este script entrena modelos baseline y el modelo final de red neuronal
para predicción de abandono estudiantil.
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

def load_modeling_data():
    """
    Carga los datos preparados para modelado.
    
    Returns:
        Tuple con características y variable objetivo
    """
    logger.info("📂 Cargando datos para modelado...")
    
    processed_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    
    # Cargar características
    features_path = processed_dir / "modeling_features.csv"
    target_path = processed_dir / "modeling_target.csv"
    
    if not features_path.exists() or not target_path.exists():
        raise FileNotFoundError("No se encontraron los archivos de datos para modelado. Ejecute primero el script de preprocesamiento.")
    
    features_df = pd.read_csv(features_path)
    target = pd.read_csv(target_path).squeeze()
    
    logger.info(f"✅ Cargados datos con {len(features_df)} registros y {len(features_df.columns)} características")
    logger.info(f"✅ Distribución de la variable objetivo: {target.value_counts().to_dict()}")
    
    return features_df, target

def train_baseline_models(features_df, target):
    """
    Entrena modelos baseline (Logistic Regression y Random Forest).
    
    Args:
        features_df: DataFrame con características
        target: Series con variable objetivo
        
    Returns:
        Diccionario con resultados de los modelos baseline
    """
    logger.info("🚀 Entrenando modelos baseline...")
    
    baseline_results = {}
    
    # Modelos baseline a entrenar
    baseline_models = {
        'logistic_regression': 'logistic',
        'random_forest': 'random_forest'
    }
    
    for model_name, model_type in baseline_models.items():
        logger.info(f"🔧 Entrenando {model_name}...")
        
        # Crear y entrenar modelo
        model = BaselineModel(model_type=model_type)
        
        # Entrenar modelo
        metrics = model.train(features_df, target)
        
        # Validación cruzada
        cv_metrics = model.cross_validate(features_df, target)
        
        # Guardar importancia de características
        feature_importance = None # Inicializar
        if model.model_type in ['logistic', 'random_forest']:
            try:
                feature_importance = model.get_feature_importance(features_df)
                if not feature_importance.empty:
                    importance_path = Path(__file__).parent.parent.parent / "docs" / "modeling" / "feature_importance"
                    importance_path.mkdir(parents=True, exist_ok=True)
                    feature_importance.to_csv(importance_path / f"{model_name}_feature_importance.csv", index=False)
                    logger.info(f"✅ Importancia de características guardada para {model_name}")
            except Exception as e:
                logger.warning(f"❌ Error al guardar importancia de características para {model_name}: {e}")
        
        # Guardar modelo
        models_dir = Path(__file__).parent.parent.parent / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        model_path = models_dir / f"{model_name}_model.pkl"
        model.save_model(str(model_path))
        
        # Guardar resultados
        baseline_results[model_name] = {
            'model_type': model_type,
            'metrics': metrics,
            'cv_metrics': cv_metrics,
            'feature_importance': feature_importance, # Guardar la importancia si se generó
            'model_path': str(model_path)
        }
        
        logger.info(f"✅ {model_name} entrenado - F1: {metrics['f1_score']:.3f}, ROC-AUC: {metrics['roc_auc']:.3f}")
    
    return baseline_results

def train_neural_network(features_df, target):
    """
    Entrena el modelo de red neuronal.
    
    Args:
        features_df: DataFrame con características
        target: Series con variable objetivo
        
    Returns:
        Diccionario con resultados del modelo de red neuronal
    """
    logger.info("🚀 Entrenando modelo de red neuronal...")
    
    # Crear modelo de red neuronal
    input_dim = len(features_df.columns)
    nn_model = NeuralNetworkModel(input_dim=input_dim, architecture=[128, 64, 32])
    
    # Entrenar modelo
    metrics = nn_model.train(features_df, target, epochs=10, batch_size=32, patience=10)
    
    # Guardar modelo
    models_dir = Path(__file__).parent.parent.parent / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "neural_network_model.pkl"
    nn_model.save_model(str(model_path))
    
    # Guardar gráficos de entrenamiento
    plots_dir = Path(__file__).parent.parent.parent / "docs" / "modeling" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    training_plot_path = plots_dir / "neural_network_training_history.png"
    nn_model.plot_training_history(str(training_plot_path))
    
    # Resultados del modelo
    nn_results = {
        'model_type': 'MLP',
        'metrics': metrics,
        'architecture': nn_model.architecture,
        'model_path': str(model_path),
        'training_plot': str(training_plot_path)
    }
    
    logger.info(f"✅ Red neuronal entrenada - F1: {metrics['f1_score']:.3f}, ROC-AUC: {metrics['roc_auc']:.3f}")
    
    return nn_results

def evaluate_models(baseline_results, nn_results, features_df, target):
    """
    Evalúa todos los modelos entrenados.
    
    Args:
        baseline_results: Resultados de modelos baseline
        nn_results: Resultados del modelo de red neuronal
        features_df: DataFrame con características
        target: Series con variable objetivo
        
    Returns:
        Diccionario con evaluaciones completas
    """
    logger.info("📊 Evaluando todos los modelos...")
    
    evaluator = ModelEvaluator()
    all_results = {}
    
    # Evaluar modelos baseline
    for model_name, results in baseline_results.items():
        logger.info(f"📋 Evaluando {model_name}...")
        
        # Cargar modelo
        model = BaselineModel(model_type=results['model_type'])
        model.load_model(results['model_path'])
        
        # Hacer predicciones
        y_pred = model.predict(features_df)
        y_pred_proba = model.predict_proba(features_df)
        if len(y_pred_proba.shape) > 1:
            y_pred_proba = y_pred_proba[:, 1]
        
        # Generar reporte de evaluación
        evaluation_report = evaluator.generate_evaluation_report(
            y_true=target.values,
            y_pred=y_pred,
            y_pred_proba=y_pred_proba,
            model_name=model_name,
            feature_importance=results['feature_importance'],
            save_dir=str(Path(__file__).parent.parent.parent / "docs" / "modeling" / "plots")
        )
        
        all_results[model_name] = evaluation_report
    
    # Evaluar modelo de red neuronal
    logger.info("📋 Evaluando red neuronal...")
    
    nn_model = NeuralNetworkModel(input_dim=len(features_df.columns))
    nn_model.load_model(nn_results['model_path'])
    
    y_pred = nn_model.predict(features_df)
    y_pred_proba = nn_model.predict_proba(features_df)
    
    evaluation_report = evaluator.generate_evaluation_report(
        y_true=target.values,
        y_pred=y_pred,
        y_pred_proba=y_pred_proba,
        model_name='neural_network',
        save_dir=str(Path(__file__).parent.parent.parent / "docs" / "modeling" / "plots")
    )
    
    all_results['neural_network'] = evaluation_report
    
    # Comparar modelos
    comparison_df = evaluator.compare_models(all_results)
    
    # Guardar comparación
    output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    comparison_path = output_dir / "model_comparison.csv"
    comparison_df.to_csv(comparison_path, index=False)
    
    logger.info(f"✅ Comparación de modelos guardada en {comparison_path}")
    logger.info("🏆 Ranking de modelos por F1-Score:")
    for i, row in comparison_df.iterrows():
        logger.info(f"   {i+1}. {row['Modelo']}: F1={row['F1-Score']:.3f}, ROC-AUC={row['ROC-AUC']:.3f}")
    
    return all_results, comparison_df

def save_training_results(baseline_results, nn_results, evaluation_results, comparison_df):
    """
    Guarda todos los resultados del entrenamiento.
    
    Args:
        baseline_results: Resultados de modelos baseline
        nn_results: Resultados del modelo de red neuronal
        evaluation_results: Resultados de evaluación
        comparison_df: DataFrame de comparación
    """
    logger.info("💾 Guardando resultados del entrenamiento...")
    
    # Crear directorio de resultados
    results_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar resultados completos
    training_results = {
        'baseline_models': baseline_results,
        'neural_network': nn_results,
        'evaluation_results': evaluation_results,
        'model_comparison': comparison_df.to_dict('records')
    }
    
    results_path = results_dir / "training_results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(training_results, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info(f"✅ Resultados completos guardados en {results_path}")

def main():
    """
    Función principal del script de entrenamiento.
    """
    logger.info("🚀 Iniciando entrenamiento de modelos...")
    
    try:
        # Cargar datos
        features_df, target = load_modeling_data()
        
        # Entrenar modelos baseline
        baseline_results = train_baseline_models(features_df, target)
        
        # Entrenar modelo de red neuronal
        nn_results = train_neural_network(features_df, target)
        
        # Evaluar todos los modelos
        evaluation_results, comparison_df = evaluate_models(baseline_results, nn_results, features_df, target)
        
        # Guardar resultados
        save_training_results(baseline_results, nn_results, evaluation_results, comparison_df)
        
        logger.info("✅ Entrenamiento completado exitosamente")
        
        return baseline_results, nn_results, evaluation_results, comparison_df
        
    except Exception as e:
        logger.error(f"❌ Error en entrenamiento: {e}")
        raise

if __name__ == "__main__":
    main()
