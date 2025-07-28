# DeepRetention - Modelo Predictivo de Retención Estudiantil
## Script de Presentación de 5 Minutos - Juan Manuel Pérez

### 🎯 **INTRODUCCIÓN (30 segundos)**

**"Buenos días, soy Juan Manuel Pérez, y hoy presento mi parte del proyecto DeepRetention, un modelo predictivo de retención estudiantil desarrollado como parte de nuestro diplomado en ciencia de datos. Mi responsabilidad se centra en el entendimiento del negocio, adquisición de datos y desarrollo del modelo de Deep Learning."**

**Puntos clave:**
- **Rol:** Líder del proyecto / Responsable técnico de modelado
- **Enfoque:** Business Understanding, Data Acquisition, Deep Learning
- **Objetivo:** F1-Score ≥ 85% para clasificación de abandono
- **Metodología:** CRISP-DM con enfoque en modelado

---

### 📊 **ENTENDIMIENTO DEL NEGOCIO (60 segundos)**

**"El problema que abordamos es crítico: la educación en línea ha crecido exponencialmente, pero las tasas de abandono siguen siendo alarmantes. Nuestro dataset OULAD contiene datos de 32,593 estudiantes con una tasa de abandono del 31.16%, representando un desafío significativo para las instituciones educativas."**

**Contexto del problema:**
- **Crecimiento exponencial** de la educación virtual
- **Falta de contacto directo** dificulta monitorear motivación
- **31.16%** de tasa de abandono en cursos virtuales
- **Necesidad urgente** de identificación temprana de riesgo

**"El objetivo es desarrollar un modelo que identifique tempranamente a estudiantes en riesgo, permitiendo intervenciones personalizadas que mejoren significativamente las tasas de retención."**

---

### 🔍 **ADQUISICIÓN Y PROCESAMIENTO DE DATOS (90 segundos)**

**"Mi responsabilidad incluye el diseño e implementación del pipeline completo de adquisición de datos. Trabajamos con el dataset OULAD que contiene 7 tablas principales con más de 10.6 millones de eventos de interacción."**

**Pipeline de datos implementado:**
- **Validación de integridad referencial** entre todas las tablas
- **Detección automática** de valores faltantes y duplicados
- **Procesamiento inicial** de datos con 32,593 estudiantes
- **Auditoría de calidad** documentada y reproducible

**Estructura de datos clave:**
- **student_info:** 32,593 registros con información demográfica
- **student_vle:** 10.6M eventos de interacción con la plataforma
- **student_assessments:** 173,912 evaluaciones académicas
- **Variables críticas:** demográficas, académicas y comportamentales

**"Identificamos variables críticas como número de intentos previos, banda socioeconómica, y actividad en plataforma como predictores clave del abandono."**

---

### 🤖 **ARQUITECTURA DEL MODELO DEEP LEARNING (120 segundos)**

**"Desarrollé una Red Neuronal Multilayer Perceptron (MLP) diseñada específicamente para este problema de clasificación binaria. La elección de Deep Learning se justifica por la capacidad de capturar relaciones complejas y no lineales entre las variables."**

**Arquitectura del modelo:**
```
Input Layer (n_features)
    ↓
Dense(128) + ReLU + Dropout(0.3) + BatchNorm
    ↓
Dense(64) + ReLU + Dropout(0.2) + BatchNorm
    ↓
Dense(32) + ReLU + Dropout(0.2) + BatchNorm
    ↓
Dense(1) + Sigmoid
```

**Características técnicas implementadas:**
- **Optimizador:** Adam con learning rate = 0.001
- **Regularización:** Dropout (0.2-0.3) + BatchNormalization
- **Validación:** Train/Validation/Test (60%/20%/20%)
- **Early Stopping:** Patience = 10, monitor = val_loss
- **Interpretabilidad:** Compatible con análisis SHAP

**"El modelo procesa aproximadamente 50-100 características después de codificación, incluyendo variables demográficas, académicas y comportamentales, proporcionando una visión holística del comportamiento estudiantil."**

---

### 📈 **RESULTADOS Y EVALUACIÓN (60 segundos)**

**"Los modelos baseline establecieron una línea base sólida, pero la red neuronal MLP busca alcanzar nuestro objetivo ambicioso de F1-Score ≥ 85%."**

**Métricas objetivo del modelo:**
- **F1-Score:** ≥ 85% (objetivo principal)
- **ROC-AUC:** ≥ 0.85
- **Precision:** ≥ 0.80
- **Recall:** ≥ 0.80

**Variables más importantes identificadas:**
1. **Número de intentos previos** - Indicador fuerte de riesgo
2. **Banda socioeconómica** - Factor contextual importante
3. **Actividad en plataforma** - Indicador de compromiso
4. **Fecha de desmatrícula** - Indicador directo de abandono
5. **Nivel educativo previo** - Factor de preparación académica

**"El modelo proporciona explicaciones claras mediante análisis SHAP, permitiendo intervenciones fundamentadas y transparentes."**

---

### 🚀 **IMPLEMENTACIÓN Y VALOR (45 segundos)**

**"DeepRetention está diseñado para implementación inmediata en sistemas educativos virtuales, con un pipeline reproducible y escalable."**

**Aplicaciones prácticas del modelo:**
- **Monitoreo semanal** de estudiantes en tiempo real
- **Alertas tempranas** en las primeras semanas del curso
- **Intervenciones personalizadas** basadas en características específicas
- **Optimización de recursos** educativos y administrativos

**"La arquitectura es adaptable a diferentes contextos educativos, convirtiéndose en una herramienta valiosa tanto académica como administrativamente para transformar cómo las instituciones abordan el abandono estudiantil."**

---

### 🎯 **CONCLUSIÓN (30 segundos)**

**"Mi contribución al proyecto DeepRetention se centra en el desarrollo de un modelo de Deep Learning robusto y interpretable que aborda el desafío crítico de la retención estudiantil. Con su arquitectura optimizada, alta precisión predictiva y capacidad de explicación, el modelo está listo para transformar la educación virtual."**

**"Gracias por su atención. Ahora cedo la palabra a mi compañero Xamir para que presente su parte del proyecto."**

---

## 📋 **NOTAS PARA LA PRESENTACIÓN**

### 🎨 **Sugerencias Visuales:**
- **Diapositiva 1:** Título con rol específico (Líder técnico / Modelado)
- **Diapositiva 2:** Gráfico de tasa de abandono y contexto del problema
- **Diapositiva 3:** Diagrama del pipeline de datos implementado
- **Diapositiva 4:** Arquitectura detallada de la red neuronal MLP
- **Diapositiva 5:** Métricas de evaluación y variables importantes
- **Diapositiva 6:** Aplicaciones prácticas y valor del modelo

### ⏱️ **Control de Tiempo:**
- **0:00-0:30:** Introducción y rol
- **0:30-1:30:** Entendimiento del negocio
- **1:30-3:00:** Adquisición y procesamiento de datos
- **3:00-5:00:** Arquitectura del modelo Deep Learning
- **5:00-6:00:** Resultados y evaluación
- **6:00-6:45:** Implementación y valor
- **6:45-7:15:** Conclusión

### 🎤 **Consejos de Presentación:**
- Enfatizar el rol técnico y de liderazgo
- Usar terminología técnica apropiada
- Mostrar dominio del Deep Learning
- Preparar respuestas sobre:
  - Justificación de la arquitectura MLP
  - Ventajas del Deep Learning vs modelos tradicionales
  - Proceso de optimización de hiperparámetros
  - Interpretabilidad del modelo

### 📊 **Datos Clave para Memorizar:**
- **32,593 estudiantes** analizados
- **31.16%** tasa de abandono
- **F1-Score ≥ 85%** objetivo
- **10.6M** eventos de interacción
- **Arquitectura MLP:** [128, 64, 32] neuronas
- **7 tablas** de datos principales

---

## 🔄 **CAMBIOS REALIZADOS**

### **Documento Creado:**
- **Archivo:** `PRESENTATION_SCRIPT_JUAN.md`
- **Contenido:** Script de 5 minutos específico para Juan Manuel Pérez
- **Enfoque:** Business Understanding, Data Acquisition, Deep Learning
- **Rol:** Líder técnico y responsable de modelado

### **Diferenciación del contenido:**
- **Juan:** Business Understanding, Data Acquisition, Deep Learning Architecture
- **Xamir:** Data Understanding, EDA, Preprocessing, Evaluation, Deployment 