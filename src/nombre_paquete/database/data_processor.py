"""
Módulo para procesar y guardar los datos limpios del dataset OULAD.

Este módulo contiene funciones para crear la estructura de carpetas,
procesar los datos y guardarlos en formato limpio para el análisis.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def create_processed_data_folder() -> Path:
    """
    Crea la carpeta para datos procesados si no existe.
    
    Returns:
        Path: Ruta de la carpeta de datos procesados
    """
    processed_path = Path("data/processed")
    processed_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Carpeta de datos procesados creada: {processed_path}")
    return processed_path

def save_processed_data(data_dict: Dict[str, pd.DataFrame], output_path: Path) -> None:
    """
    Guarda los DataFrames procesados en archivos CSV.
    
    Args:
        data_dict: Diccionario con DataFrames a guardar
        output_path: Ruta donde guardar los archivos
    """
    logger.info("💾 Guardando datos procesados...")
    
    for name, df in data_dict.items():
        file_path = output_path / f"{name}.csv"
        df.to_csv(file_path, index=False)
        logger.info(f"✅ Guardado {name}.csv: {len(df)} registros")
    
    logger.info("✅ Todos los datos procesados guardados exitosamente")

def merge_student_data(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Crea un DataFrame consolidado con toda la información del estudiante.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        pd.DataFrame: DataFrame consolidado con información del estudiante
    """
    logger.info("🔗 Consolidando información del estudiante...")
    
    # DataFrame base con información demográfica
    student_base = data_dict['student_info'].copy()
    
    # Agregar información de registro
    registration_info = data_dict['student_registration'][
        ['id_student', 'code_module', 'code_presentation', 'date_registration', 'date_unregistration']
    ]
    
    # Merge con información de registro
    student_consolidated = student_base.merge(
        registration_info,
        on=['id_student', 'code_module', 'code_presentation'],
        how='left'
    )
    
    # Agregar información de cursos
    course_info = data_dict['courses'][
        ['code_module', 'code_presentation', 'module_presentation_length']
    ]
    
    student_consolidated = student_consolidated.merge(
        course_info,
        on=['code_module', 'code_presentation'],
        how='left'
    )
    
    logger.info(f"✅ Información consolidada: {len(student_consolidated)} registros")
    return student_consolidated

def create_interaction_features(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Crea características agregadas de las interacciones estudiantiles.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        pd.DataFrame: DataFrame con características de interacciones
    """
    logger.info("📊 Creando características de interacciones...")
    
    student_vle = data_dict['student_vle'].copy()
    
    # Agregar información del VLE
    vle_info = data_dict['vle'][['id_site', 'activity_type']].drop_duplicates()
    student_vle = student_vle.merge(vle_info, on='id_site', how='left')
    
    # Características agregadas por estudiante y semana
    interaction_features = student_vle.groupby(['id_student', 'code_module', 'code_presentation', 'date']).agg({
        'sum_click': ['sum', 'count', 'mean'],
        'activity_type': 'nunique'
    }).reset_index()
    
    # Renombrar columnas
    interaction_features.columns = [
        'id_student', 'code_module', 'code_presentation', 'date',
        'total_clicks', 'interaction_count', 'avg_clicks_per_interaction', 'unique_activity_types'
    ]
    
    logger.info(f"✅ Características de interacciones creadas: {len(interaction_features)} registros")
    return interaction_features

def create_assessment_features(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Crea características agregadas de las evaluaciones estudiantiles.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        pd.DataFrame: DataFrame con características de evaluaciones
    """
    logger.info("📊 Creando características de evaluaciones...")
    
    student_assessments = data_dict['student_assessments'].copy()
    assessments = data_dict['assessments'].copy()
    
    # Merge con información de evaluaciones
    assessment_features = student_assessments.merge(
        assessments[['id_assessment', 'assessment_type', 'weight']],
        on='id_assessment',
        how='left'
    )
    
    # Características agregadas por estudiante
    student_assessment_summary = assessment_features.groupby('id_student').agg({
        'score': ['mean', 'std', 'min', 'max', 'count'],
        'date_submitted': ['mean', 'std'],
        'assessment_type': 'nunique',
        'weight': 'sum'
    }).reset_index()
    
    # Renombrar columnas
    student_assessment_summary.columns = [
        'id_student',
        'avg_score', 'std_score', 'min_score', 'max_score', 'assessment_count',
        'avg_submission_date', 'std_submission_date', 'unique_assessment_types', 'total_weight'
    ]
    
    logger.info(f"✅ Características de evaluaciones creadas: {len(student_assessment_summary)} registros")
    return student_assessment_summary

def process_all_data(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Procesa todos los datos y crea DataFrames consolidados para el análisis.
    
    Args:
        data_dict: Diccionario con todos los DataFrames originales
        
    Returns:
        Dict[str, pd.DataFrame]: Diccionario con DataFrames procesados
    """
    logger.info("🔄 Procesando todos los datos...")
    
    processed_data = {}
    
    # 1. Información consolidada del estudiante
    processed_data['student_consolidated'] = merge_student_data(data_dict)
    
    # 2. Características de interacciones
    processed_data['interaction_features'] = create_interaction_features(data_dict)
    
    # 3. Características de evaluaciones
    processed_data['assessment_features'] = create_assessment_features(data_dict)
    
    # 4. Datos originales limpios
    for name, df in data_dict.items():
        processed_data[f"{name}_clean"] = df.copy()
    
    logger.info("✅ Procesamiento de datos completado")
    return processed_data 