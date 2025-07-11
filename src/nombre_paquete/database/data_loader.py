"""
Módulo para cargar los datos del dataset OULAD.

Este módulo contiene funciones para cargar cada archivo CSV del dataset
y realizar validaciones básicas de formato.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta base de los datos
DATA_PATH = Path("data/anonymisedData")

def load_student_info() -> pd.DataFrame:
    """
    Carga el archivo studentInfo.csv con información demográfica y académica.
    
    Returns:
        pd.DataFrame: DataFrame con información de estudiantes
    """
    try:
        file_path = DATA_PATH / "studentInfo.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado studentInfo.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando studentInfo.csv: {e}")
        raise

def load_courses() -> pd.DataFrame:
    """
    Carga el archivo courses.csv con información de cursos.
    
    Returns:
        pd.DataFrame: DataFrame con información de cursos
    """
    try:
        file_path = DATA_PATH / "courses.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado courses.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando courses.csv: {e}")
        raise

def load_assessments() -> pd.DataFrame:
    """
    Carga el archivo assessments.csv con información de evaluaciones.
    
    Returns:
        pd.DataFrame: DataFrame con información de evaluaciones
    """
    try:
        file_path = DATA_PATH / "assessments.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado assessments.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando assessments.csv: {e}")
        raise

def load_student_assessments() -> pd.DataFrame:
    """
    Carga el archivo studentAssessment.csv con resultados de evaluaciones.
    
    Returns:
        pd.DataFrame: DataFrame con resultados de evaluaciones
    """
    try:
        file_path = DATA_PATH / "studentAssessment.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado studentAssessment.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando studentAssessment.csv: {e}")
        raise

def load_student_registration() -> pd.DataFrame:
    """
    Carga el archivo studentRegistration.csv con información de registro.
    
    Returns:
        pd.DataFrame: DataFrame con información de registro
    """
    try:
        file_path = DATA_PATH / "studentRegistration.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado studentRegistration.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando studentRegistration.csv: {e}")
        raise

def load_vle() -> pd.DataFrame:
    """
    Carga el archivo vle.csv con información del entorno virtual.
    
    Returns:
        pd.DataFrame: DataFrame con información del VLE
    """
    try:
        file_path = DATA_PATH / "vle.csv"
        df = pd.read_csv(file_path)
        logger.info(f"✅ Cargado vle.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando vle.csv: {e}")
        raise

def load_student_vle() -> pd.DataFrame:
    """
    Carga el archivo studentVle.csv con interacciones estudiantiles.
    
    Returns:
        pd.DataFrame: DataFrame con interacciones estudiantiles
    """
    try:
        file_path = DATA_PATH / "studentVle.csv"
        # Cargar en chunks debido al tamaño del archivo
        chunk_size = 100000
        chunks = []
        
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            chunks.append(chunk)
        
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"✅ Cargado studentVle.csv: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"❌ Error cargando studentVle.csv: {e}")
        raise

def load_all_data() -> Dict[str, pd.DataFrame]:
    """
    Carga todos los archivos del dataset OULAD.
    
    Returns:
        Dict[str, pd.DataFrame]: Diccionario con todos los DataFrames
    """
    logger.info("🚀 Iniciando carga de todos los datos del dataset OULAD...")
    
    data_dict = {
        'student_info': load_student_info(),
        'courses': load_courses(),
        'assessments': load_assessments(),
        'student_assessments': load_student_assessments(),
        'student_registration': load_student_registration(),
        'vle': load_vle(),
        'student_vle': load_student_vle()
    }
    
    logger.info("✅ Carga de datos completada exitosamente")
    return data_dict

def get_data_summary() -> Dict[str, Any]:
    """
    Genera un resumen de todos los datos cargados.
    
    Returns:
        Dict[str, Any]: Resumen con estadísticas de cada archivo
    """
    data_dict = load_all_data()
    summary = {}
    
    for name, df in data_dict.items():
        summary[name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'missing_values': df.isnull().sum().sum()
        }
    
    return summary 