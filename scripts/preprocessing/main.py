"""
Script principal de preprocesamiento para el modelo de retención estudiantil.

Este script carga los datos procesados, crea características relevantes
y prepara los datasets para entrenamiento de modelos.
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Añadir el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from nombre_paquete.preprocessing.feature_engineering import FeatureEngineer
from nombre_paquete.database.data_loader import load_all_data

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_processed_data():
    """
    Carga los datos procesados disponibles.
    
    Returns:
        Tuple con DataFrames de estudiantes e interacciones
    """
    logger.info("📂 Cargando datos procesados...")
    
    processed_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    
    # Cargar datos de estudiantes
    student_files = [
        'student_consolidated.csv',
        'student_info_clean.csv'
    ]
    
    student_df = None
    for file in student_files:
        file_path = processed_dir / file
        if file_path.exists():
            student_df = pd.read_csv(file_path)
            logger.info(f"✅ Cargado {file} con {len(student_df)} registros")
            break
    
    if student_df is None:
        raise FileNotFoundError("No se encontró ningún archivo de datos de estudiantes procesados")
    
    # Cargar características de interacciones
    interaction_df = None
    interaction_file = processed_dir / 'interaction_features.csv'
    if interaction_file.exists():
        interaction_df = pd.read_csv(interaction_file)
        logger.info(f"✅ Cargado interaction_features.csv con {len(interaction_df)} registros")
    
    return student_df, interaction_df

def prepare_modeling_data():
    """
    Prepara los datos para modelado.
    
    Returns:
        Tuple con características y variable objetivo
    """
    logger.info("🔧 Preparando datos para modelado...")
    
    # Cargar datos
    student_df, interaction_df = load_processed_data()
    
    # Crear ingeniero de características
    feature_engineer = FeatureEngineer()
    
    # Preparar características
    features_df, target = feature_engineer.prepare_features(
        student_df=student_df,
        interaction_features=interaction_df
    )
    
    # Guardar características preparadas
    output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    features_path = output_dir / "modeling_features.csv"
    target_path = output_dir / "modeling_target.csv"
    
    features_df.to_csv(features_path, index=False)
    target.to_csv(target_path, index=False)
    
    logger.info(f"✅ Características guardadas en {features_path}")
    logger.info(f"✅ Variable objetivo guardada en {target_path}")
    
    # Mostrar resumen de características
    logger.info(f"📊 Resumen de características:")
    logger.info(f"   - Total de características: {len(feature_engineer.feature_columns)}")
    logger.info(f"   - Características numéricas: {len(feature_engineer.numerical_columns)}")
    logger.info(f"   - Características categóricas: {len(feature_engineer.categorical_columns)}")
    logger.info(f"   - Distribución de la variable objetivo:")
    logger.info(f"     {target.value_counts().to_dict()}")
    
    return features_df, target, feature_engineer

def create_feature_importance_report(feature_engineer, features_df, target):
    """
    Crea un reporte de importancia de características.
    
    Args:
        feature_engineer: Instancia del ingeniero de características
        features_df: DataFrame con características
        target: Series con variable objetivo
    """
    logger.info("📊 Generando reporte de importancia de características...")
    
    # Crear DataFrame con características y target para correlación
    features_with_target = features_df.copy()
    features_with_target['target'] = target
    
    # Calcular ranking de importancia
    importance_ranking = feature_engineer.get_feature_importance_ranking(features_with_target)
    
    if not importance_ranking.empty:
        # Guardar ranking
        output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
        ranking_path = output_dir / "feature_importance_ranking.csv"
        importance_ranking.to_csv(ranking_path, index=False)
        
        logger.info(f"✅ Ranking de importancia guardado en {ranking_path}")
        logger.info("📈 Top 10 características más importantes:")
        for i, row in importance_ranking.head(10).iterrows():
            logger.info(f"   {i+1}. {row['feature']}: {row['correlation']:.3f}")
    
    return importance_ranking

def main():
    """
    Función principal del script de preprocesamiento.
    """
    logger.info("🚀 Iniciando preprocesamiento de datos para modelado...")
    
    try:
        # Preparar datos para modelado
        features_df, target, feature_engineer = prepare_modeling_data()
        
        # Crear reporte de importancia de características
        importance_ranking = create_feature_importance_report(feature_engineer, features_df, target)
        
        # Guardar información del feature engineer
        output_dir = Path(__file__).parent.parent.parent / "data" / "processed"
        feature_info = {
            'feature_columns': feature_engineer.feature_columns,
            'numerical_columns': feature_engineer.numerical_columns,
            'categorical_columns': feature_engineer.categorical_columns,
            'total_features': len(feature_engineer.feature_columns)
        }
        
        # Guardar como JSON
        import json
        feature_info_path = output_dir / "feature_info.json"
        with open(feature_info_path, 'w', encoding='utf-8') as f:
            json.dump(feature_info, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Información de características guardada en {feature_info_path}")
        logger.info("✅ Preprocesamiento completado exitosamente")
        
        return features_df, target, feature_engineer
        
    except Exception as e:
        logger.error(f"❌ Error en preprocesamiento: {e}")
        raise

if __name__ == "__main__":
    main()
