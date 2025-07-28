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
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import numbers

# Añadir el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from nombre_paquete.models.baseline_model import BaselineModel
from nombre_paquete.models.neural_network import NeuralNetworkModel
from nombre_paquete.evaluation.model_evaluator import ModelEvaluator

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_metrics(metrics_dict):
    """
    Convierte todos los valores numéricos de un diccionario a float nativo de Python,
    manejando arrays de numpy de un solo elemento.
    """
    cleaned_metrics = {}
    for key, value in metrics_dict.items():
        if isinstance(value, np.ndarray) and value.size == 1:
            cleaned_metrics[key] = value.item()
        elif isinstance(value, numbers.Number):
            cleaned_metrics[key] = float(value)
        else:
            # Mantener valores no numéricos si los hubiera
            cleaned_metrics[key] = value
    return cleaned_metrics

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

    # Iniciar experimento de MLflow para modelos baseline
    mlflow.set_experiment("Baseline Models")
    
    for model_name, model_type in baseline_models.items():
        with mlflow.start_run(run_name=model_name):
            logger.info(f"🔧 Entrenando {model_name}...")
            
            # Registrar parámetros del modelo
            mlflow.log_param("model_type", model_type)

            # Crear y entrenar modelo
            model = BaselineModel(model_type=model_type)
            
            # Entrenar modelo
            results = model.train(features_df, target)
            
            # Separar métricas de otros artefactos
            metrics_to_log = {k: v for k, v in results.items() if isinstance(v, numbers.Number) or (isinstance(v, np.ndarray) and v.size == 1)}
            cleaned_metrics = clean_metrics(metrics_to_log)
            
            # Registrar métricas de entrenamiento
            mlflow.log_metrics(cleaned_metrics)

            # Guardar reporte de clasificación como artefacto de texto
            if 'classification_report' in results:
                mlflow.log_text(results['classification_report'], "classification_report.txt")
            
            # Guardar matriz de confusión como artefacto
            if 'confusion_matrix' in results:
                np.savetxt("confusion_matrix.txt", results['confusion_matrix'], fmt='%d')
                mlflow.log_artifact("confusion_matrix.txt", "confusion_matrix")

            # Validación cruzada
            cv_results = model.cross_validate(features_df, target)
            
            # Separar métricas de la lista de scores
            cv_metrics_to_log = {k: v for k, v in cv_results.items() if isinstance(v, numbers.Number)}
            cleaned_cv_metrics = clean_metrics(cv_metrics_to_log)
            cv_metrics_renamed = {f"cv_{k}": v for k, v in cleaned_cv_metrics.items()}
            mlflow.log_metrics(cv_metrics_renamed)

            # Guardar los scores de cada fold como un artefacto
            if 'test_score' in cv_results:
                np.savetxt("cv_test_scores.txt", cv_results['test_score'])
                mlflow.log_artifact("cv_test_scores.txt", "cross_validation")

            # Inferir firma del modelo
            X_sample = features_df.head()
            y_pred_sample = model.predict(X_sample)
            signature = infer_signature(X_sample, y_pred_sample)

            # Registrar modelo en MLflow
            mlflow.sklearn.log_model(
                sk_model=model.pipeline,
                artifact_path=model_name,
                signature=signature
            )
            
            # Guardar importancia de características como artefacto
            feature_importance = None
            if model.model_type in ['logistic', 'random_forest']:
                try:
                    feature_importance = model.get_feature_importance(features_df)
                    if not feature_importance.empty:
                        importance_path = Path(__file__).parent.parent.parent / "data" / "temp_artifacts"
                        importance_path.mkdir(parents=True, exist_ok=True)
                        importance_csv = importance_path / f"{model_name}_feature_importance.csv"
                        feature_importance.to_csv(importance_csv, index=False)
                        mlflow.log_artifact(str(importance_csv), "feature_importance")
                        logger.info(f"✅ Importancia de características registrada para {model_name}")
                except Exception as e:
                    logger.warning(f"❌ Error al registrar importancia de características para {model_name}: {e}")
            
            # Guardar resultados (ya no se guarda el modelo aquí)
            run_id = mlflow.active_run().info.run_id
            baseline_results[model_name] = {
                'model_type': model_type,
                'metrics': metrics_to_log, # Guardar solo las métricas numéricas
                'cv_metrics': cv_results,
                'feature_importance': feature_importance,
                'mlflow_run_id': run_id
            }
            
            logger.info(f"✅ {model_name} entrenado y registrado en MLflow (Run ID: {run_id})")
    
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

    mlflow.set_experiment("Neural Network")

    with mlflow.start_run(run_name="MLP"):
        # Crear modelo de red neuronal
        input_dim = len(features_df.columns)
        architecture = [128, 64, 32]
        nn_model = NeuralNetworkModel(input_dim=input_dim, architecture=architecture)

        # Registrar parámetros
        mlflow.log_param("input_dim", input_dim)
        mlflow.log_param("architecture", str(architecture))
        mlflow.log_param("epochs", 10)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("patience", 10)

        # Entrenar modelo
        results = nn_model.train(features_df, target, epochs=10, batch_size=32, patience=10)
        
        # Separar métricas de otros artefactos
        metrics_to_log = {k: v for k, v in results.items() if isinstance(v, numbers.Number) or (isinstance(v, np.ndarray) and v.size == 1)}
        cleaned_metrics = clean_metrics(metrics_to_log)
        
        # Registrar métricas
        mlflow.log_metrics(cleaned_metrics)

        # Guardar reporte de clasificación como artefacto de texto
        if 'classification_report' in results:
            mlflow.log_text(results['classification_report'], "classification_report.txt")

        # Guardar matriz de confusión como artefacto
        if 'confusion_matrix' in results:
            np.savetxt("confusion_matrix.txt", results['confusion_matrix'], fmt='%d')
            mlflow.log_artifact("confusion_matrix.txt", "confusion_matrix")

        # Inferir firma y registrar modelo
        X_sample = features_df.head()
        y_pred_sample = nn_model.predict(X_sample)
        signature = infer_signature(X_sample, y_pred_sample)
        
        # MLflow no tiene un "flavor" nativo de Keras/TF como con sklearn.
        # Guardamos el modelo manualmente y lo registramos como artefacto.
        temp_model_dir = Path(__file__).parent.parent.parent / "data" / "temp_artifacts" / "nn_model"
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        model_path = temp_model_dir / "neural_network_model.pkl"
        nn_model.save_model(str(model_path))
        mlflow.log_artifacts(str(temp_model_dir), artifact_path="model")

        # Guardar gráficos de entrenamiento como artefacto
        plots_dir = Path(__file__).parent.parent.parent / "data" / "temp_artifacts"
        training_plot_path = plots_dir / "neural_network_training_history.png"
        nn_model.plot_training_history(str(training_plot_path))
        mlflow.log_artifact(str(training_plot_path), "plots")

        # Resultados del modelo
        run_id = mlflow.active_run().info.run_id
        nn_results = {
            'model_type': 'MLP',
            'metrics': metrics_to_log, # Guardar solo las métricas numéricas
            'architecture': nn_model.architecture,
            'mlflow_run_id': run_id,
            'training_plot': str(training_plot_path)
        }
        
        logger.info(f"✅ Red neuronal entrenada y registrada en MLflow (Run ID: {run_id})")
    
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
    
    # Cargar la lista de características numéricas usadas en el entrenamiento
    feature_info_path = Path(__file__).parent.parent.parent / "data" / "processed" / "feature_info.json"
    with open(feature_info_path, 'r') as f:
        feature_info = json.load(f)
    numerical_features = feature_info['numerical_columns']
    
    # Asegurarse de que el DataFrame de evaluación solo tenga esas columnas
    features_df_eval = features_df[numerical_features]
    
    evaluator = ModelEvaluator()
    all_results = {}
    
    # Evaluar modelos baseline
    for model_name, results in baseline_results.items():
        logger.info(f"📋 Evaluando {model_name}...")
        
        # Cargar modelo desde MLflow
        run_id = results['mlflow_run_id']
        model_uri = f"runs:/{run_id}/{model_name}"
        model = mlflow.sklearn.load_model(model_uri)
        
        # Hacer predicciones usando solo las columnas correctas
        y_pred = model.predict(features_df_eval)
        y_pred_proba = model.predict_proba(features_df_eval)
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

    # Cargar modelo de red neuronal desde MLflow
    run_id = nn_results['mlflow_run_id']
    # Como no es un "flavor" nativo, cargamos manualmente el artefacto
    # y usamos nuestra clase de modelo para cargarlo.
    client = mlflow.tracking.MlflowClient()
    local_path = client.download_artifacts(run_id, "model")
    
    nn_model = NeuralNetworkModel(input_dim=len(numerical_features)) # Usar el número correcto de dims
    nn_model.load_model(os.path.join(local_path, "neural_network_model.pkl"))

    y_pred = nn_model.predict(features_df_eval)
    y_pred_proba = nn_model.predict_proba(features_df_eval)
    
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
