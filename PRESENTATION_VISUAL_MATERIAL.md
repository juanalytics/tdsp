# DeepRetention - Modelo Predictivo de Retención Estudiantil
## Material Visual para Presentación

---

## 🎯 **PRESENTACIÓN DE JUAN MANUEL PÉREZ**

### **Diapositiva 1: Introducción**
```
┌─────────────────────────────────────────────────────────┐
│                    DeepRetention                       │
│           Modelo Predictivo de Retención Estudiantil   │
│                                                         │
│  Juan Manuel Pérez                                     │
│  Líder del Proyecto / Responsable Técnico de Modelado  │
│                                                         │
│  • Business Understanding                              │
│  • Data Acquisition                                    │
│  • Deep Learning Architecture                          │
│                                                         │
│  Objetivo: F1-Score ≥ 85%                             │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 2: Entendimiento del Negocio**
```
┌─────────────────────────────────────────────────────────┐
│              EL PROBLEMA CRÍTICO                       │
│                                                         │
│  📈 Educación en línea: Crecimiento exponencial        │
│  ❌ Falta de contacto directo                          │
│  📊 31.16% tasa de abandono                           │
│  🚨 Necesidad urgente de identificación temprana       │
│                                                         │
│  Dataset OULAD:                                        │
│  • 32,593 estudiantes                                 │
│  • 10.6M eventos de interacción                       │
│  • 7 tablas principales                               │
│                                                         │
│  Objetivo: Intervenciones personalizadas               │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 3: Adquisición y Procesamiento de Datos**
```
┌─────────────────────────────────────────────────────────┐
│              PIPELINE DE DATOS                         │
│                                                         │
│  🔍 Validación de integridad referencial              │
│  🔍 Detección automática de valores faltantes         │
│  🔍 Auditoría de calidad documentada                  │
│                                                         │
│  Estructura de Datos:                                  │
│  ┌─────────────────┬─────────────┬─────────────────┐   │
│  │ Tabla           │ Registros   │ Descripción     │   │
│  ├─────────────────┼─────────────┼─────────────────┤   │
│  │ student_info    │ 32,593      │ Info demográfica│   │
│  │ student_vle     │ 10.6M       │ Interacciones   │   │
│  │ assessments     │ 173,912     │ Evaluaciones    │   │
│  └─────────────────┴─────────────┴─────────────────┘   │
│                                                         │
│  Variables críticas identificadas:                     │
│  • Número de intentos previos                         │
│  • Banda socioeconómica                               │
│  • Actividad en plataforma                            │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 4: Arquitectura del Modelo Deep Learning**
```
┌─────────────────────────────────────────────────────────┐
│           ARQUITECTURA MLP                            │
│                                                         │
│  Input Layer (n_features)                              │
│           ↓                                             │
│  Dense(128) + ReLU + Dropout(0.3) + BatchNorm         │
│           ↓                                             │
│  Dense(64) + ReLU + Dropout(0.2) + BatchNorm          │
│           ↓                                             │
│  Dense(32) + ReLU + Dropout(0.2) + BatchNorm          │
│           ↓                                             │
│  Dense(1) + Sigmoid                                    │
│                                                         │
│  Características Técnicas:                             │
│  • Optimizador: Adam (lr=0.001)                       │
│  • Regularización: Dropout + BatchNorm                │
│  • Validación: Train/Val/Test (60%/20%/20%)          │
│  • Early Stopping: Patience=10                        │
│  • Interpretabilidad: Compatible con SHAP             │
│                                                         │
│  Procesa ~50-100 características                       │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 5: Resultados y Evaluación**
```
┌─────────────────────────────────────────────────────────┐
│              MÉTRICAS OBJETIVO                        │
│                                                         │
│  🎯 F1-Score: ≥ 85% (Objetivo principal)             │
│  📊 ROC-AUC: ≥ 0.85                                   │
│  📈 Precision: ≥ 0.80                                 │
│  📉 Recall: ≥ 0.80                                    │
│                                                         │
│  Variables Más Importantes:                            │
│  ┌─────────────────┬─────────────────────────────────┐ │
│  │ Variable        │ Descripción                    │ │
│  ├─────────────────┼─────────────────────────────────┤ │
│  │ prev_attempts   │ Indicador fuerte de riesgo     │ │
│  │ imd_band        │ Factor contextual              │ │
│  │ sum_click       │ Indicador de compromiso        │ │
│  │ date_unreg      │ Indicador directo              │ │
│  │ education       │ Factor de preparación          │ │
│  └─────────────────┴─────────────────────────────────┘ │
│                                                         │
│  ✅ Explicaciones claras con SHAP                      │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 6: Implementación y Valor**
```
┌─────────────────────────────────────────────────────────┐
│              APLICACIONES PRÁCTICAS                   │
│                                                         │
│  🔔 Monitoreo semanal de estudiantes                  │
│  ⚠️  Alertas tempranas en primeras semanas           │
│  🎯 Intervenciones personalizadas                     │
│  💰 Optimización de recursos educativos               │
│                                                         │
│  Características del Pipeline:                         │
│  • Reproducible y escalable                           │
│  • Adaptable a diferentes contextos                   │
│  • Herramienta académica y administrativa             │
│                                                         │
│  Impacto Esperado:                                     │
│  • Transformación del abordaje del abandono           │
│  • Mejora significativa en retención                  │
│  • Intervenciones más efectivas                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 **PRESENTACIÓN DE XAMIR ERNESTO ROJAS**

### **Diapositiva 1: Introducción**
```
┌─────────────────────────────────────────────────────────┐
│                    DeepRetention                       │
│           Modelo Predictivo de Retención Estudiantil   │
│                                                         │
│  Xamir Ernesto Rojas                                   │
│  Analista de Datos / Preprocesamiento y Evaluación     │
│                                                         │
│  • Data Understanding                                  │
│  • EDA y Preprocessing                                 │
│  • Evaluation y Deployment                             │
│                                                         │
│  Objetivo: Calidad de datos y evaluación robusta       │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 2: Entendimiento de Datos**
```
┌─────────────────────────────────────────────────────────┐
│              ANÁLISIS DE CALIDAD                      │
│                                                         │
│  Dataset OULAD:                                        │
│  • 7 tablas principales                               │
│  • 32,593 estudiantes                                 │
│  • 10.6M eventos de interacción                       │
│                                                         │
│  Problemas Identificados:                              │
│  ┌─────────────────┬─────────────┬─────────────────┐   │
│  │ Problema        │ Cantidad    │ Porcentaje      │   │
│  ├─────────────────┼─────────────┼─────────────────┤   │
│  │ Valores faltantes│ 1,111       │ 3.41%          │   │
│  │ Duplicados      │ 787,170     │ Múltiples       │   │
│  │ Tipos incorrectos│ Varios      │ Corregidos      │   │
│  └─────────────────┴─────────────┴─────────────────┘   │
│                                                         │
│  Distribución Variable Objetivo:                       │
│  • Pass: 38% (12,361)                                 │
│  • Withdrawn: 31% (10,156) ← Objetivo                 │
│  • Fail: 22% (7,052)                                  │
│  • Distinction: 9% (3,024)                            │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 3: Análisis Exploratorio y Preprocesamiento**
```
┌─────────────────────────────────────────────────────────┐
│           VARIABLES MÁS RELEVANTES                    │
│                                                         │
│  Ranking de Importancia:                               │
│  ┌─────┬─────────────────────┬──────────────────────┐  │
│  │ #   │ Variable            │ Descripción          │  │
│  ├─────┼─────────────────────┼──────────────────────┤  │
│  │ 1   │ num_of_prev_attempts│ Correlación fuerte   │  │
│  │ 2   │ imd_band           │ Indicador socioeconómico│  │
│  │ 3   │ highest_education  │ Nivel educativo previo│  │
│  │ 4   │ sum_click          │ Actividad en plataforma│  │
│  │ 5   │ score              │ Rendimiento académico │  │
│  └─────┴─────────────────────┴──────────────────────┘  │
│                                                         │
│  Proceso de Preprocesamiento:                          │
│  🔧 Limpieza de datos                                 │
│  🔧 Feature engineering                                │
│  🔧 One-hot encoding                                   │
│  🔧 StandardScaler                                     │
│  🔧 5-fold validación cruzada                         │
│                                                         │
│  ✅ Datos de alta calidad para el modelo              │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 4: Evaluación y Validación del Modelo**
```
┌─────────────────────────────────────────────────────────┐
│              MÉTRICAS DE EVALUACIÓN                   │
│                                                         │
│  Métricas Implementadas:                               │
│  🎯 F1-Score: ≥ 85% (Objetivo principal)             │
│  📊 ROC-AUC: ≥ 0.85                                   │
│  📈 Precision: ≥ 0.80                                 │
│  📉 Recall: ≥ 0.80                                    │
│  📊 Accuracy: ≥ 0.85                                  │
│                                                         │
│  Validación Cruzada:                                   │
│  • Train/Validation/Test: 60%/20%/20%                 │
│  • Stratified Sampling                                 │
│  • 5-fold Cross-Validation                            │
│  • Early Stopping                                      │
│                                                         │
│  Análisis de Interpretabilidad:                        │
│  🔍 SHAP Analysis                                     │
│  🔍 Feature Importance                                │
│  🔍 Partial Dependence Plots                          │
│  🔍 Local Interpretability                            │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 5: Despliegue y Pipeline Reproducible**
```
┌─────────────────────────────────────────────────────────┐
│              PIPELINE REPRODUCIBLE                     │
│                                                         │
│  Componentes del Pipeline:                             │
│  ┌─────────────────┬─────────────────────────────────┐ │
│  │ Componente      │ Descripción                    │ │
│  ├─────────────────┼─────────────────────────────────┤ │
│  │ Data Pipeline   │ Carga, limpieza, preprocesamiento│ │
│  │ Model Pipeline  │ Entrenamiento, validación      │ │
│  │ Evaluation      │ Métricas automáticas           │ │
│  │ Deployment      │ Preparación para implementación │ │
│  └─────────────────┴─────────────────────────────────┘ │
│                                                         │
│  Características Técnicas:                             │
│  🔄 Reproducibilidad: Seeds fijos                     │
│  📈 Escalabilidad: Arquitectura adaptable             │
│  📊 Monitoreo: Métricas continuas                     │
│  📚 Documentación: Código comentado                   │
│                                                         │
│  ✅ Listo para implementación inmediata               │
└─────────────────────────────────────────────────────────┘
```

### **Diapositiva 6: Resultados y Aplicaciones Prácticas**
```
┌─────────────────────────────────────────────────────────┐
│              APLICACIONES PRÁCTICAS                   │
│                                                         │
│  Sistemas Implementados:                               │
│  🚨 Sistema de alertas tempranas                      │
│  📊 Dashboard de monitoreo                             │
│  🎯 Intervenciones personalizadas                     │
│  💰 Optimización de recursos                          │
│                                                         │
│  Impacto Esperado:                                     │
│  ┌─────────────────┬─────────────────────────────────┐ │
│  │ Métrica         │ Resultado Esperado              │ │
│  ├─────────────────┼─────────────────────────────────┤ │
│  │ Abandono        │ Reducción significativa          │ │
│  │ Retención       │ Mejora sustancial               │ │
│  │ Recursos        │ Optimización eficiente          │ │
│  │ Intervenciones  │ Más efectivas y personalizadas  │ │
│  └─────────────────┴─────────────────────────────────┘ │
│                                                         │
│  ✅ Transformación de datos en acciones concretas     │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 **DATOS CLAVE PARA AMBAS PRESENTACIONES**

### **Estadísticas Principales:**
- **32,593 estudiantes** analizados
- **31.16%** tasa de abandono
- **10.6M** eventos de interacción
- **7 tablas** principales de datos
- **F1-Score ≥ 85%** objetivo
- **4 semanas** de desarrollo

### **Variables Críticas:**
1. **num_of_prev_attempts** - Indicador fuerte de riesgo
2. **imd_band** - Factor socioeconómico
3. **highest_education** - Nivel educativo previo
4. **sum_click** - Actividad en plataforma
5. **score** - Rendimiento académico

### **Métricas Objetivo:**
- **F1-Score:** ≥ 85%
- **ROC-AUC:** ≥ 0.85
- **Precision:** ≥ 0.80
- **Recall:** ≥ 0.80
- **Accuracy:** ≥ 0.85

---

## 🎨 **INSTRUCCIONES DE USO**

### **Para Juan Manuel:**
1. Mostrar diapositivas 1-6 de su sección
2. Enfatizar el rol técnico y de liderazgo
3. Usar terminología de Deep Learning
4. Transición suave a Xamir

### **Para Xamir:**
1. Mostrar diapositivas 1-6 de su sección
2. Enfatizar análisis de datos y calidad
3. Mostrar dominio de evaluación
4. Conclusión con preguntas

### **Elementos Visuales:**
- Usar colores consistentes
- Mantener formato claro y legible
- Incluir iconos y emojis para claridad
- Asegurar que los datos sean visibles desde lejos

### **Timing:**
- Cada diapositiva corresponde a ~45-60 segundos
- Transiciones suaves entre secciones
- Pausas para preguntas al final 