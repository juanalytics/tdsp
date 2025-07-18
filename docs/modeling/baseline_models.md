# Reporte del Modelo Baseline

Este documento contiene los resultados de los modelos baseline implementados para la predicción de retención estudiantil.

## Descripción del modelo

Los modelos baseline son modelos simples que se utilizan para establecer una línea base de rendimiento antes de implementar modelos más complejos. En este proyecto, se implementaron dos modelos baseline:

1. **Regresión Logística**: Modelo lineal simple que establece una línea base de rendimiento
2. **Random Forest**: Modelo de ensemble que proporciona una línea base más robusta

## Variables de entrada

Las características utilizadas en los modelos baseline incluyen:

### Características Demográficas
- **Género**: Codificado como variables dummy (gender_M, gender_F)
- **Grupo de edad**: Codificado como variables dummy (age_band_<35, age_band_35-55, age_band_55+)
- **Nivel educativo previo**: Codificado como variables dummy
- **Región**: Codificado como variables dummy
- **Discapacidad**: Codificado como variables dummy
- **Banda socioeconómica**: Convertida a escala numérica (1-10)

### Características Académicas
- **Número de intentos previos**: Variable numérica
- **Tiene intentos previos**: Variable binaria (0/1)
- **Múltiples intentos previos**: Variable binaria (0/1)
- **Créditos estudiados**: Variable numérica
- **Es tiempo completo**: Variable binaria (≥120 créditos)
- **Es tiempo parcial**: Variable binaria (<120 créditos)
- **Semana de registro**: Variable numérica
- **Registro temprano**: Variable binaria (≤0 días)
- **Registro tardío**: Variable binaria (>0 días)
- **Tiene desmatrícula**: Variable binaria
- **Semana de desmatrícula**: Variable numérica
- **Longitud del módulo en semanas**: Variable numérica

### Características Comportamentales (si están disponibles)
- **Total de clics**: Variable numérica
- **Actividad alta**: Variable binaria (>mediana)
- **Actividad baja**: Variable binaria (≤mediana)
- **Actividad consistente**: Variable binaria (>0 clics/semana)
- **Compromiso a largo plazo**: Variable binaria (>mediana semanas activas)

## Variable objetivo

La variable objetivo es `final_result` convertida a binaria:
- **0**: No abandono (Pass, Fail, Distinction)
- **1**: Abandono (Withdrawn)

## Evaluación del modelo

### Métricas de evaluación

Se utilizan las siguientes métricas para evaluar el rendimiento:

- **Accuracy**: Proporción de predicciones correctas
- **Precision**: Proporción de predicciones positivas correctas
- **Recall**: Proporción de casos positivos identificados correctamente
- **F1-Score**: Media armónica de precision y recall
- **ROC-AUC**: Área bajo la curva ROC
- **Average Precision**: Media de precision para diferentes umbrales de recall

### Resultados de evaluación esperados

| Modelo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|--------|----------|-----------|--------|----------|---------|
| Regresión Logística | ~0.70-0.75 | ~0.65-0.70 | ~0.60-0.65 | ~0.62-0.67 | ~0.75-0.80 |
| Random Forest | ~0.75-0.80 | ~0.70-0.75 | ~0.65-0.70 | ~0.67-0.72 | ~0.80-0.85 |

## Análisis de los resultados

### Fortalezas de los modelos baseline

1. **Simplicidad**: Fáciles de interpretar y explicar
2. **Velocidad**: Entrenamiento y predicción rápidos
3. **Robustez**: Menos propensos al overfitting
4. **Interpretabilidad**: Especialmente la regresión logística

### Debilidades de los modelos baseline

1. **Capacidad limitada**: Pueden no capturar relaciones complejas
2. **Linealidad**: La regresión logística asume relaciones lineales
3. **Rendimiento**: Pueden no alcanzar el objetivo de F1-Score ≥ 85%

### Características más importantes

Basado en el análisis de correlación y importancia de características, se espera que las variables más relevantes sean:

1. **Número de intentos previos**: Indicador fuerte de riesgo de abandono
2. **Banda socioeconómica**: Factor contextual importante
3. **Actividad en la plataforma**: Indicador de compromiso
4. **Fecha de desmatrícula**: Indicador directo de abandono
5. **Nivel educativo previo**: Factor de preparación académica

## Conclusiones

Los modelos baseline proporcionan una línea base sólida para comparar con modelos más complejos. Se espera que:

1. El Random Forest supere a la Regresión Logística en la mayoría de métricas
2. Ningún modelo baseline alcance el objetivo de F1-Score ≥ 85%
3. Las características comportamentales mejoren significativamente el rendimiento
4. Los modelos sirvan como validación de la calidad de los datos y características

## Referencias

- Scikit-learn: Machine Learning in Python
- Open University Learning Analytics Dataset (OULAD)
- CRISP-DM Methodology
- Student Retention Prediction Literature
