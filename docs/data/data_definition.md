# Definición de los datos

## Origen de los datos

- **Fuente:** Open University Learning Analytics Dataset (OULAD), descargado y almacenado en la carpeta `data/anonymisedData/`.
- **Archivos originales:**
  - `studentInfo.csv`, `studentVle.csv`, `studentRegistration.csv`, `studentAssessment.csv`, `courses.csv`, `assessments.csv`, `vle.csv`.
- **Descripción:** Datos demográficos, académicos y de interacción de estudiantes en cursos virtuales.

## Especificación de los scripts para la carga de datos

- **Script principal:** `scripts/data_acquisition/main.py`
  - Carga todos los archivos CSV originales.
  - Valida integridad, tipos y valores faltantes.
  - Procesa y limpia los datos.
  - Genera archivos procesados en `data/processed/`.
  - Genera reporte de adquisición en `docs/data/data_acquisition_report.md`.

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

- **Ubicación:** `data/anonymisedData/`
- **Estructura:** Archivos CSV planos, cada uno representando una tabla del dataset OULAD.
- **Procedimientos de transformación y limpieza:**
  - Validación de integridad referencial y tipos de datos.
  - Limpieza de valores faltantes y duplicados.
  - Generación de variables derivadas y archivos consolidados.

### Base de datos de destino

- **Ubicación:** `data/processed/`
- **Estructura:** Archivos CSV limpios y enriquecidos, listos para análisis y modelado.
- **Procedimientos de carga y transformación:**
  - Los datos procesados se guardan mediante el script de adquisición.
  - Incluyen archivos como `student_info_clean.csv`, `student_consolidated.csv`, `interaction_features.csv`, entre otros.
