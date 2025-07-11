
## ✅ Estado Actual del Proyecto

### ✅ Completado

#### 1. **Business Understanding**
- ✅ [Project Charter](docs/business_understanding/project_charter.md) - Objetivos, alcance y metodología
- ✅ Definición clara del problema y criterios de éxito

#### 2. **Data Understanding**
- ✅ [Data Definition](docs/data/data_definition.md) - Estructura y origen de los datos
- ✅ [Data Dictionary](docs/data/data_dictionary.md) - Descripción detallada de variables
- ✅ [Data Summary](docs/data/data_summary.md) - Resumen estadístico y calidad

#### 3. **Data Acquisition**
- ✅ Pipeline de carga de datos automatizado
- ✅ Validación de integridad referencial
- ✅ Detección de valores faltantes y duplicados
- ✅ Procesamiento inicial de datos
- ✅ [Reporte de adquisición](docs/data/data_acquisition_report.md)

### �� En Progreso

#### 4. **Exploratory Data Analysis (EDA)**
- 🔄 Análisis exploratorio de datos
- 🔄 Visualizaciones y estadísticas descriptivas
- 🔄 Identificación de patrones y correlaciones

### ⏳ Pendiente

#### 5. **Data Preprocessing**
- ⏳ Limpieza de valores faltantes
- ⏳ Transformación de variables
- ⏳ Feature engineering
- ⏳ Preparación para modelado

#### 6. **Modeling**
- ⏳ Desarrollo de modelos baseline
- ⏳ Entrenamiento de redes neuronales (MLP/CNN-1D)
- ⏳ Optimización de hiperparámetros
- ⏳ Validación cruzada

#### 7. **Evaluation**
- ⏳ Métricas de evaluación (F1-score, ROC-AUC)
- ⏳ Interpretación de modelos (SHAP)
- ⏳ Análisis de importancia de variables

#### 8. **Deployment**
- ⏳ Documentación final
- ⏳ Notebook reproducible
- ⏳ Pipeline completo

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
```bash
python >= 3.8
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd tdsp

# Instalar dependencias
pip install -e .
```

### Ejecutar Pipeline de Datos
```bash
# Cargar y procesar datos
python scripts/data_acquisition/main.py
```

## 📈 Métricas Clave

### Objetivos del Proyecto
- **F1-score ≥ 85%** para clasificación de abandono
- **Pipeline reproducible** y escalable
- **Análisis interpretable** de variables importantes

### Estado Actual
- **Datos cargados:** 32,593 estudiantes
- **Tasa de abandono:** 31.16%
- **Integridad de datos:** ✅ Validada
- **Calidad de datos:** Documentada

## 📊 Variables Clave Identificadas

### Variables de Alto Riesgo
1. `num_of_prev_attempts` - Intentos previos
2. `imd_band` - Indicador socioeconómico
3. `highest_education` - Nivel educativo previo
4. `final_result` - Variable objetivo (Withdrawn)

### Variables de Comportamiento
1. `sum_click` - Interacciones en plataforma
2. `score` - Rendimiento académico
3. `date_submitted` - Puntualidad en entregas

### Variables Demográficas
1. `age_band` - Grupo de edad
2. `gender` - Género
3. `region` - Región geográfica
4. `disability` - Necesidades especiales

## �� Equipo del Proyecto

- **Juan Manuel Pérez** – Líder del proyecto / Responsable técnico
- **Xamir Ernesto Rojas** – Analista de datos / Preprocesamiento

## �� Documentación

- [Project Charter](docs/business_understanding/project_charter.md)
- [Data Definition](docs/data/data_definition.md)
- [Data Dictionary](docs/data/data_dictionary.md)
- [Data Summary](docs/data/data_summary.md)
- [Data Acquisition Report](docs/data/data_acquisition_report.md)

## 🔗 Enlaces Útiles

- **Dataset OULAD:** https://analyse.kmi.open.ac.uk/#open-dataset
- **Metodología CRISP-DM:** Framework de ciencia de datos
- **Deep Learning:** TensorFlow/Keras para redes neuronales

## 📝 Licencia

Este proyecto se desarrolla en el marco de un diplomado académico. Los datos utilizados son de acceso abierto con licencia académica.

---

**Última actualización:** Julio 2024  
**Estado:** Data Understanding completado, iniciando EDA
