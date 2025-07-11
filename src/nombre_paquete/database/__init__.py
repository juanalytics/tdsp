"""
Módulo de base de datos para el proyecto DeepRetention.

Este módulo contiene funciones para cargar, validar y procesar los datos del dataset OULAD.
"""

from .data_loader import (
    load_student_info,
    load_courses,
    load_assessments,
    load_student_assessments,
    load_student_registration,
    load_vle,
    load_student_vle,
    load_all_data
)

from .data_validator import (
    validate_data_integrity,
    check_missing_values,
    validate_data_types,
    generate_data_summary
)

from .data_processor import (
    create_processed_data_folder,
    save_processed_data,
    merge_student_data
)

__all__ = [
    # Data loading functions
    'load_student_info',
    'load_courses', 
    'load_assessments',
    'load_student_assessments',
    'load_student_registration',
    'load_vle',
    'load_student_vle',
    'load_all_data',
    
    # Data validation functions
    'validate_data_integrity',
    'check_missing_values',
    'validate_data_types',
    'generate_data_summary',
    
    # Data processing functions
    'create_processed_data_folder',
    'save_processed_data',
    'merge_student_data'
]
