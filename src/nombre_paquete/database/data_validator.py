"""
Módulo para validar la integridad y calidad de los datos del dataset OULAD.

Este módulo contiene funciones para verificar la consistencia de los datos,
valores faltantes, tipos de datos y relaciones entre tablas.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

def validate_data_integrity(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Valida la integridad referencial entre las tablas del dataset.
    
    Args:
        data_dict: Diccionario con todos los DataFrames cargados
        
    Returns:
        Dict con resultados de validación
    """
    logger.info("🔍 Validando integridad referencial de los datos...")
    
    validation_results = {
        'referential_integrity': {},
        'data_consistency': {},
        'overall_status': 'PASS'
    }
    
    # Validar que todos los estudiantes en student_info existen en student_registration
    student_info_ids = set(data_dict['student_info']['id_student'].unique())
    registration_ids = set(data_dict['student_registration']['id_student'].unique())
    
    missing_in_registration = student_info_ids - registration_ids
    validation_results['referential_integrity']['students_in_registration'] = {
        'status': 'PASS' if len(missing_in_registration) == 0 else 'FAIL',
        'missing_count': len(missing_in_registration),
        'missing_ids': list(missing_in_registration)[:10]  # Solo primeros 10 para reporte
    }
    
    # Validar que todos los módulos en student_info existen en courses
    student_modules = set(tuple(x) for x in data_dict['student_info'][['code_module', 'code_presentation']].drop_duplicates().values.tolist())
    course_modules = set(tuple(x) for x in data_dict['courses'][['code_module', 'code_presentation']].drop_duplicates().values.tolist())
    
    missing_in_courses = student_modules - course_modules
    validation_results['referential_integrity']['modules_in_courses'] = {
        'status': 'PASS' if len(missing_in_courses) == 0 else 'FAIL',
        'missing_count': len(missing_in_courses),
        'missing_modules': list(missing_in_courses)[:10]
    }
    
    # Validar que todas las evaluaciones en student_assessments existen en assessments
    assessment_ids = set(data_dict['assessments']['id_assessment'].unique())
    student_assessment_ids = set(data_dict['student_assessments']['id_assessment'].unique())
    
    missing_in_assessments = student_assessment_ids - assessment_ids
    validation_results['referential_integrity']['assessments_reference'] = {
        'status': 'PASS' if len(missing_in_assessments) == 0 else 'FAIL',
        'missing_count': len(missing_in_assessments),
        'missing_ids': list(missing_in_assessments)[:10]
    }
    
    # Verificar consistencia general
    any_failures = any(
        result['status'] == 'FAIL' 
        for result in validation_results['referential_integrity'].values()
    )
    
    if any_failures:
        validation_results['overall_status'] = 'FAIL'
        logger.warning("⚠️ Se encontraron problemas de integridad referencial")
    else:
        logger.info("✅ Integridad referencial validada correctamente")
    
    return validation_results

def check_missing_values(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Verifica valores faltantes en todos los DataFrames.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        Dict con estadísticas de valores faltantes
    """
    logger.info("🔍 Verificando valores faltantes...")
    
    missing_summary = {}
    
    for name, df in data_dict.items():
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        
        missing_summary[name] = {
            'total_rows': len(df),
            'missing_values': missing_counts.to_dict(),
            'missing_percentages': missing_percentages.to_dict(),
            'total_missing': missing_counts.sum(),
            'total_missing_percentage': (missing_counts.sum() / len(df)) * 100
        }
    
    # Log resumen de valores faltantes
    for name, summary in missing_summary.items():
        if summary['total_missing'] > 0:
            logger.warning(f"⚠️ {name}: {summary['total_missing']} valores faltantes ({summary['total_missing_percentage']:.2f}%)")
        else:
            logger.info(f"✅ {name}: Sin valores faltantes")
    
    return missing_summary

def validate_data_types(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Valida que los tipos de datos sean los esperados según el diccionario de datos.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        Dict con resultados de validación de tipos
    """
    logger.info("🔍 Validando tipos de datos...")
    
    # Definir tipos esperados según el data dictionary
    expected_types = {
        'student_info': {
            'code_module': 'object',
            'code_presentation': 'object',
            'id_student': 'int64',
            'gender': 'object',
            'region': 'object',
            'highest_education': 'object',
            'imd_band': 'object',
            'age_band': 'object',
            'num_of_prev_attempts': 'int64',
            'studied_credits': 'int64',
            'disability': 'object',
            'final_result': 'object'
        },
        'courses': {
            'code_module': 'object',
            'code_presentation': 'object',
            'module_presentation_length': 'int64'
        },
        'assessments': {
            'code_module': 'object',
            'code_presentation': 'object',
            'id_assessment': 'int64',
            'assessment_type': 'object',
            'date': 'object',  # Puede contener strings vacíos
            'weight': 'int64'
        },
        'student_assessments': {
            'id_assessment': 'int64',
            'id_student': 'int64',
            'date_submitted': 'int64',
            'is_banked': 'int64',
            'score': 'int64'
        },
        'student_registration': {
            'code_module': 'object',
            'code_presentation': 'object',
            'id_student': 'int64',
            'date_registration': 'int64',
            'date_unregistration': 'object'  # Puede contener strings vacíos
        },
        'vle': {
            'id_site': 'int64',
            'code_module': 'object',
            'code_presentation': 'object',
            'activity_type': 'object',
            'week_from': 'object',  # Puede contener strings vacíos
            'week_to': 'object'     # Puede contener strings vacíos
        },
        'student_vle': {
            'code_module': 'object',
            'code_presentation': 'object',
            'id_student': 'int64',
            'id_site': 'int64',
            'date': 'int64',
            'sum_click': 'int64'
        }
    }
    
    type_validation = {}
    
    for name, df in data_dict.items():
        if name in expected_types:
            actual_types = df.dtypes.to_dict()
            expected = expected_types[name]
            
            mismatches = {}
            for col, expected_type in expected.items():
                if col in actual_types:
                    actual_type = str(actual_types[col])
                    if actual_type != expected_type:
                        mismatches[col] = {
                            'expected': expected_type,
                            'actual': actual_type
                        }
            
            type_validation[name] = {
                'status': 'PASS' if len(mismatches) == 0 else 'FAIL',
                'mismatches': mismatches,
                'total_columns': len(expected),
                'mismatched_columns': len(mismatches)
            }
    
    # Log resultados
    for name, result in type_validation.items():
        if result['status'] == 'PASS':
            logger.info(f"✅ {name}: Tipos de datos correctos")
        else:
            logger.warning(f"⚠️ {name}: {result['mismatched_columns']} columnas con tipos incorrectos")
    
    return type_validation

def generate_data_summary(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Genera un resumen completo de todos los datos cargados.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        
    Returns:
        Dict con resumen completo de datos
    """
    logger.info("📊 Generando resumen completo de datos...")
    
    summary = {
        'file_summary': {},
        'data_quality': {},
        'key_statistics': {}
    }
    
    # Resumen por archivo
    for name, df in data_dict.items():
        summary['file_summary'][name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'duplicate_rows': df.duplicated().sum(),
            'missing_values': df.isnull().sum().sum()
        }
    
    # Estadísticas clave para student_info
    if 'student_info' in data_dict:
        student_df = data_dict['student_info']
        summary['key_statistics']['students'] = {
            'total_students': len(student_df),
            'unique_modules': student_df['code_module'].nunique(),
            'unique_presentations': student_df['code_presentation'].nunique(),
            'gender_distribution': student_df['gender'].value_counts().to_dict(),
            'final_result_distribution': student_df['final_result'].value_counts().to_dict(),
            'withdrawal_rate': (student_df['final_result'] == 'Withdrawn').mean() * 100
        }
    
    # Estadísticas para student_vle (interacciones)
    if 'student_vle' in data_dict:
        vle_df = data_dict['student_vle']
        summary['key_statistics']['interactions'] = {
            'total_interactions': len(vle_df),
            'unique_students': vle_df['id_student'].nunique(),
            'avg_clicks_per_interaction': vle_df['sum_click'].mean(),
            'total_clicks': vle_df['sum_click'].sum()
        }
    
    logger.info("✅ Resumen de datos generado exitosamente")
    return summary 