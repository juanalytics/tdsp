# Definición de los datos

## Origen de los datos

El dataset utilizado es el **Open University Learning Analytics Dataset (OULAD)**, un conjunto de datos abierto y ampliamente utilizado en investigaciones de analítica educativa. Este dataset contiene información anonimizada de estudiantes de la Open University del Reino Unido, incluyendo datos demográficos, académicos y de comportamiento en plataformas virtuales de aprendizaje.

**Fuente:** https://analyse.kmi.open.ac.uk/#open-dataset
**Licencia:** Academic License (uso académico sin restricciones)
**Tamaño total:** Aproximadamente 433MB de datos

## Especificación de los scripts para la carga de datos

Los scripts para la carga inicial de los datos se encuentran en `scripts/data_acquisition/main.py`. Este script se encarga de:
- Leer los archivos CSV originales del dataset OULAD
- Realizar una inspección inicial de la calidad de los datos
- Validar la integridad de los datos
- Guardar los datos en el formato requerido para el análisis posterior

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

**Ubicación de los archivos de origen:** `data/anonymisedData/`

**Estructura de los archivos de origen:**

1. **`courses.csv`** (526B, 24 líneas)
   - Contiene información sobre los cursos disponibles
   - Variables: `code_module`, `code_presentation`, `module_presentation_length`
   - 7 módulos diferentes (AAA, BBB, CCC, DDD, EEE, FFF, GGG)
   - Diferentes presentaciones por año (2013J, 2014J, 2013B, 2014B)

2. **`studentInfo.csv`** (3.3MB)
   - Información demográfica y académica de los estudiantes
   - Variables: `code_module`, `code_presentation`, `id_student`, `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `num_of_prev_attempts`, `studied_credits`, `disability`, `final_result`
   - Contiene datos de 32,593 estudiantes aproximadamente

3. **`studentRegistration.csv`** (1.1MB)
   - Registros de matrícula y desmatrícula de estudiantes
   - Variables: `code_module`, `code_presentation`, `id_student`, `date_registration`, `date_unregistration`
   - Información sobre cuándo se registraron y desregistraron los estudiantes

4. **`assessments.csv`** (8.0KB, 208 líneas)
   - Información sobre las evaluaciones de cada curso
   - Variables: `code_module`, `code_presentation`, `id_assessment`, `assessment_type`, `date`, `weight`
   - Tipos de evaluación: TMA (Tutor Marked Assignment), Exam, CMA (Computer Marked Assignment)

5. **`studentAssessment.csv`** (5.4MB)
   - Resultados de las evaluaciones de los estudiantes
   - Variables: `id_assessment`, `id_student`, `date_submitted`, `is_banked`, `score`
   - Contiene las calificaciones y fechas de entrega

6. **`vle.csv`** (254KB, 6366 líneas)
   - Información sobre los recursos del entorno virtual de aprendizaje
   - Variables: `id_site`, `code_module`, `code_presentation`, `activity_type`, `week_from`, `week_to`
   - Tipos de actividad: resource, oucontent, url, forumng, glossary, etc.

7. **`studentVle.csv`** (433MB)
   - Registros detallados de interacciones de estudiantes con la plataforma virtual
   - Variables: `code_module`, `code_presentation`, `id_student`, `id_site`, `date`, `sum_click`
   - Contiene aproximadamente 10.6 millones de eventos de interacción

**Procedimientos de transformación y limpieza de los datos:**
- Validación de integridad referencial entre tablas
- Conversión de tipos de datos (fechas, números, categorías)
- Manejo de valores nulos y datos faltantes
- Normalización de variables categóricas
- Creación de variables derivadas para el análisis

### Base de datos de destino

**Base de datos de destino:** Para la fase de EDA, los datos procesados se almacenan en:
- Archivos CSV limpios en `data/processed/`
- Base de datos SQLite temporal en `data/processed/oulad.db` (opcional)

**Estructura de la base de datos de destino:**
- **Tabla `students`:** Información demográfica y académica consolidada
- **Tabla `courses`:** Información de cursos y módulos
- **Tabla `assessments`:** Evaluaciones y sus resultados
- **Tabla `interactions`:** Interacciones con la plataforma virtual agregadas por estudiante y semana
- **Tabla `features`:** Variables derivadas y características para el modelado

**Procedimientos de carga y transformación:**
- El script de preprocesamiento (`scripts/preprocessing/main.py`) se encarga de:
  - Limpiar y validar los datos originales
  - Crear variables derivadas relevantes para la predicción de abandono
  - Agregar interacciones semanales por estudiante
  - Generar características temporales y de comportamiento
  - Exportar datos listos para el análisis exploratorio y modelado
