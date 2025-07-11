#!/usr/bin/env python3
"""
Script principal para la adquisición de datos del dataset OULAD.

Este script carga todos los archivos CSV del dataset, valida su integridad,
procesa los datos y los guarda en formato limpio para el análisis posterior.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar el módulo
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from nombre_paquete.database import (
    load_all_data,
    validate_data_integrity,
    check_missing_values,
    validate_data_types,
    generate_data_summary,
    create_processed_data_folder,
    save_processed_data
)
from nombre_paquete.database.data_processor import process_all_data

import logging
import pandas as pd

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Función principal que ejecuta todo el pipeline de adquisición de datos.
    """
    logger.info("🚀 Iniciando pipeline de adquisición de datos OULAD...")
    
    try:
        # 1. Cargar todos los datos
        logger.info("📥 Paso 1: Cargando datos del dataset OULAD...")
        data_dict = load_all_data()
        
        # 2. Validar integridad de datos
        logger.info("🔍 Paso 2: Validando integridad de datos...")
        integrity_results = validate_data_integrity(data_dict)
        
        # 3. Verificar valores faltantes
        logger.info("🔍 Paso 3: Verificando valores faltantes...")
        missing_results = check_missing_values(data_dict)
        
        # 4. Validar tipos de datos
        logger.info("🔍 Paso 4: Validando tipos de datos...")
        type_results = validate_data_types(data_dict)
        
        # 5. Generar resumen de datos
        logger.info("📊 Paso 5: Generando resumen de datos...")
        data_summary = generate_data_summary(data_dict)
        
        # 6. Crear carpeta de datos procesados
        logger.info("📁 Paso 6: Creando estructura de carpetas...")
        processed_path = create_processed_data_folder()
        
        # 7. Procesar datos
        logger.info("🔄 Paso 7: Procesando datos...")
        processed_data = process_all_data(data_dict)
        
        # 8. Guardar datos procesados
        logger.info("💾 Paso 8: Guardando datos procesados...")
        save_processed_data(processed_data, processed_path)
        
        # 9. Generar reporte final
        logger.info("📋 Paso 9: Generando reporte final...")
        generate_final_report(data_dict, integrity_results, missing_results, type_results, data_summary)
        
        logger.info("✅ Pipeline de adquisición de datos completado exitosamente!")
        
    except Exception as e:
        logger.error(f"❌ Error en el pipeline de adquisición de datos: {e}")
        raise

def generate_final_report(data_dict, integrity_results, missing_results, type_results, data_summary):
    """
    Genera un reporte final con todos los resultados de la validación.
    
    Args:
        data_dict: Diccionario con todos los DataFrames
        integrity_results: Resultados de validación de integridad
        missing_results: Resultados de verificación de valores faltantes
        type_results: Resultados de validación de tipos
        data_summary: Resumen de datos
    """
    logger.info("📋 Generando reporte final de adquisición de datos...")
    
    # Crear carpeta de reportes si no existe
    reports_path = Path("docs/data")
    reports_path.mkdir(parents=True, exist_ok=True)
    
    # Generar reporte en markdown
    report_content = f"""# Reporte de Adquisición de Datos - Dataset OULAD

## Resumen Ejecutivo

Fecha de ejecución: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

### Estado General: {'✅ EXITOSO' if integrity_results['overall_status'] == 'PASS' else '❌ CON PROBLEMAS'}

## Estadísticas de Archivos

"""
    
    # Agregar estadísticas por archivo
    for name, summary in data_summary['file_summary'].items():
        report_content += f"""
### {name.replace('_', ' ').title()}
- **Registros:** {summary['rows']:,}
- **Columnas:** {summary['columns']}
- **Memoria:** {summary['memory_mb']:.2f} MB
- **Valores faltantes:** {summary['missing_values']:,}
- **Filas duplicadas:** {summary['duplicate_rows']:,}

"""
    
    # Agregar estadísticas clave
    if 'key_statistics' in data_summary:
        if 'students' in data_summary['key_statistics']:
            students_stats = data_summary['key_statistics']['students']
            report_content += f"""
## Estadísticas Clave de Estudiantes

- **Total de estudiantes:** {students_stats['total_students']:,}
- **Módulos únicos:** {students_stats['unique_modules']}
- **Presentaciones únicas:** {students_stats['unique_presentations']}
- **Tasa de abandono:** {students_stats['withdrawal_rate']:.2f}%

### Distribución por Género
"""
            for gender, count in students_stats['gender_distribution'].items():
                report_content += f"- {gender}: {count:,}\n"
            
            report_content += f"""
### Distribución por Resultado Final
"""
            for result, count in students_stats['final_result_distribution'].items():
                report_content += f"- {result}: {count:,}\n"
    
    # Agregar información de interacciones
    if 'key_statistics' in data_summary and 'interactions' in data_summary['key_statistics']:
        interaction_stats = data_summary['key_statistics']['interactions']
        report_content += f"""
## Estadísticas de Interacciones

- **Total de interacciones:** {interaction_stats['total_interactions']:,}
- **Estudiantes únicos:** {interaction_stats['unique_students']:,}
- **Promedio de clics por interacción:** {interaction_stats['avg_clicks_per_interaction']:.2f}
- **Total de clics:** {interaction_stats['total_clicks']:,}

"""
    
    # Agregar resultados de validación
    report_content += f"""
## Resultados de Validación

### Integridad Referencial
"""
    for check_name, result in integrity_results['referential_integrity'].items():
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        report_content += f"- {check_name}: {status_icon} {result['status']}\n"
    
    # Guardar reporte
    report_file = reports_path / "data_acquisition_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logger.info(f"✅ Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main()
