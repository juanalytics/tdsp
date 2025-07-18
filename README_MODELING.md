# Modeling Stage - Student Retention Prediction

Este documento describe la implementación de la etapa de modelado para el proyecto de predicción de retención estudiantil siguiendo la metodología CRISP-DM.

## 📋 Descripción General

La etapa de modelado incluye:
- **Preprocesamiento**: Ingeniería de características y preparación de datos
- **Modelos Baseline**: Regresión Logística y Random Forest
- **Modelo Final**: Red Neuronal MLP (Multilayer Perceptron)
- **Evaluación**: Métricas comprehensivas y visualizaciones

## 🏗️ Arquitectura del Proyecto

```
src/nombre_paquete/
├── preprocessing/
│   └── feature_engineering.py    # Ingeniería de características
├── models/
│   ├── baseline_model.py         # Modelos baseline
│   └── neural_network.py         # Modelo final MLP
└── evaluation/
    └── model_evaluator.py        # Evaluación de modelos

scripts/
├── preprocessing/
│   └── main.py                   # Script de preprocesamiento
├── training/
│   └── main.py                   # Script de entrenamiento
└── evaluation/
    └── main.py                   # Script de evaluación
```

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
pip install -r requirements_modeling.txt
```

### 2. Verificar Datos Procesados

Asegúrate de que los siguientes archivos estén disponibles en `data/processed/`:
- `student_consolidated.csv` o `student_info_clean.csv`
- `interaction_features.csv` (opcional)

## 📊 Flujo de Trabajo

### Paso 1: Preprocesamiento

```bash
cd scripts/preprocessing
python main.py
```

**Resultados esperados:**
- `data/processed/modeling_features.csv`
- `data/processed/modeling_target.csv`
- `data/processed/feature_importance_ranking.csv`
- `data/processed/feature_info.json`

### Paso 2: Entrenamiento

```bash
cd scripts/training
python main.py
```

**Resultados esperados:**
- `models/logistic_regression_model.pkl`
- `models/random_forest_model.pkl`
- `models/neural_network_model.pkl`
- `data/processed/training_results.json`
- `docs/modeling/plots/neural_network_training_history.png`

### Paso 3: Evaluación

```bash
cd scripts/evaluation
python main.py
```

**Resultados esperados:**
- `data/processed/evaluation_results.json`
- `data/processed/final_model_comparison.csv`
- `data/processed/evaluation_summary.json`
- `docs/modeling/plots/` (gráficos de evaluación)

## 🔧 Componentes Principales

### Feature Engineering (`src/nombre_paquete/preprocessing/feature_engineering.py`)

**Clase**: `FeatureEngineer`

**Funcionalidades:**
- Creación de características demográficas (one-hot encoding)
- Ingeniería de características académicas
- Integración de características comportamentales
- Preparación de variable objetivo binaria

**Uso:**
```python
from nombre_paquete.preprocessing.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
features_df, target = engineer.prepare_features(student_df, interaction_df)
```

### Baseline Models (`src/nombre_paquete/models/baseline_model.py`)

**Clase**: `BaselineModel`

**Modelos disponibles:**
- `logistic`: Regresión Logística
- `random_forest`: Random Forest

**Uso:**
```python
from nombre_paquete.models.baseline_model import BaselineModel

# Regresión Logística
lr_model = BaselineModel(model_type='logistic')
metrics = lr_model.train(features_df, target)

# Random Forest
rf_model = BaselineModel(model_type='random_forest')
metrics = rf_model.train(features_df, target)
```

### Neural Network (`src/nombre_paquete/models/neural_network.py`)

**Clase**: `NeuralNetworkModel`

**Arquitectura por defecto:**
- Input: n_features
- Dense(128) + ReLU + Dropout(0.3) + BatchNorm
- Dense(64) + ReLU + Dropout(0.2) + BatchNorm
- Dense(32) + ReLU + Dropout(0.2) + BatchNorm
- Dense(1) + Sigmoid

**Uso:**
```python
from nombre_paquete.models.neural_network import NeuralNetworkModel

nn_model = NeuralNetworkModel(input_dim=len(features_df.columns))
metrics = nn_model.train(features_df, target, epochs=100)
```

### Model Evaluator (`src/nombre_paquete/evaluation/model_evaluator.py`)

**Clase**: `ModelEvaluator`

**Funcionalidades:**
- Cálculo de métricas (F1, ROC-AUC, Precision, Recall)
- Generación de gráficos (matriz de confusión, ROC, Precision-Recall)
- Comparación de modelos
- Reportes de evaluación

**Uso:**
```python
from nombre_paquete.evaluation.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator()
report = evaluator.generate_evaluation_report(y_true, y_pred, y_pred_proba, 'model_name')
```

## 📈 Métricas de Evaluación

### Métricas Principales
- **F1-Score**: Objetivo ≥ 85%
- **ROC-AUC**: Área bajo la curva ROC
- **Precision**: Proporción de predicciones positivas correctas
- **Recall**: Proporción de casos positivos identificados
- **Accuracy**: Proporción total de predicciones correctas

### Interpretación
- **F1-Score ≥ 85%**: Excelente capacidad de clasificación
- **ROC-AUC ≥ 0.85**: Excelente capacidad discriminativa
- **Precision ≥ 0.80**: Baja tasa de falsos positivos
- **Recall ≥ 0.80**: Baja tasa de falsos negativos

## 📊 Visualizaciones Generadas

### Durante el Entrenamiento
- **Historial de entrenamiento**: Loss, accuracy, precision, recall vs épocas
- **Gráficos de convergencia**: Para el modelo de red neuronal

### Durante la Evaluación
- **Matriz de confusión**: Para cada modelo
- **Curva ROC**: Para cada modelo
- **Curva Precision-Recall**: Para cada modelo
- **Importancia de características**: Top características más relevantes
- **Comparación de modelos**: Gráfico de barras con métricas

## 🔍 Interpretabilidad

### Características Más Importantes
1. **Número de intentos previos**: Indicador fuerte de riesgo
2. **Banda socioeconómica**: Factor contextual importante
3. **Actividad en plataforma**: Indicador de compromiso
4. **Fecha de desmatrícula**: Indicador directo de abandono
5. **Nivel educativo previo**: Factor de preparación académica

### Técnicas de Interpretación
- **SHAP Values**: Para explicación de predicciones individuales
- **Feature Importance**: Para modelos baseline
- **Correlation Analysis**: Para entender relaciones lineales

## 🎯 Objetivos del Proyecto

### Criterios de Éxito
- ✅ **F1-Score ≥ 85%**: Capacidad de clasificación confiable
- ✅ **Pipeline automatizado**: Proceso reproducible y escalable
- ✅ **Código documentado**: Notebooks y scripts claros
- ✅ **Interpretabilidad**: Explicación de predicciones

### Metodología
- **CRISP-DM**: Cross-Industry Standard Process for Data Mining
- **Agile**: Iteraciones breves con entregables específicos
- **Deep Learning**: TensorFlow/Keras para modelo final

## 📁 Estructura de Archivos

### Entrada
```
data/processed/
├── student_consolidated.csv      # Datos de estudiantes
├── interaction_features.csv       # Características de interacciones
└── assessment_features.csv        # Características de evaluaciones
```

### Salida
```
data/processed/
├── modeling_features.csv          # Características para modelado
├── modeling_target.csv            # Variable objetivo
├── feature_importance_ranking.csv # Ranking de importancia
├── training_results.json          # Resultados de entrenamiento
├── evaluation_results.json        # Resultados de evaluación
└── final_model_comparison.csv     # Comparación final

models/
├── logistic_regression_model.pkl  # Modelo baseline 1
├── random_forest_model.pkl        # Modelo baseline 2
└── neural_network_model.pkl       # Modelo final

docs/modeling/plots/
├── neural_network_training_history.png
├── logistic_regression_confusion_matrix.png
├── random_forest_roc_curve.png
└── final_model_comparison.png
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error: "No se encontraron archivos de datos"**
   - Verifica que los archivos estén en `data/processed/`
   - Ejecuta primero el script de preprocesamiento

2. **Error: "TensorFlow no disponible"**
   - Instala TensorFlow: `pip install tensorflow`
   - Verifica la versión de Python (3.8+)

3. **Error: "Memoria insuficiente"**
   - Reduce el tamaño del batch en el modelo neural
   - Usa menos características o menos datos

4. **Error: "Modelo no converge"**
   - Ajusta el learning rate
   - Aumenta el número de épocas
   - Verifica la calidad de los datos

### Logs y Debugging
- Todos los scripts generan logs detallados
- Revisa los archivos de log para identificar problemas
- Usa `logging.basicConfig(level=logging.DEBUG)` para más detalles

## 📚 Referencias

- **Dataset**: Open University Learning Analytics Dataset (OULAD)
- **Metodología**: CRISP-DM (Cross-Industry Standard Process)
- **Deep Learning**: TensorFlow/Keras Documentation
- **Interpretabilidad**: SHAP (SHapley Additive exPlanations)

## 🤝 Contribución

Para contribuir al proyecto:
1. Sigue la estructura de archivos existente
2. Documenta nuevas funcionalidades
3. Mantén compatibilidad con el pipeline existente
4. Ejecuta todos los tests antes de commit

---

**Nota**: Este proyecto sigue la metodología CRISP-DM y está diseñado para ser reproducible y escalable en diferentes contextos educativos. 