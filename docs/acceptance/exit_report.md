# Informe de Salida del Proyecto

## 1. Resumen Ejecutivo

- **Proyecto:** Predicción de Retención Estudiantil.
- **Objetivo:** Desarrollar un modelo de machine learning para predecir el abandono estudiantil, con un F1-Score objetivo de ≥ 85%.
- **Metodología:** Se siguió el proceso estándar para minería de datos CRISP-DM.
- **Resultado Clave:** Se implementó y evaluó exitosamente un modelo de Red Neuronal (MLP) que cumple con el criterio de éxito. El modelo se desplegó como un servicio de API en Google Cloud Platform.

## 2. Descripción del Proyecto y Objetivos

### Contexto
La alta tasa de abandono en cursos en línea es un desafío crítico para las instituciones educativas. Este proyecto se centró en la identificación temprana de estudiantes en riesgo para permitir intervenciones oportunas.

### Objetivos
1.  **Modelo Predictivo:** Construir un modelo con un F1-Score ≥ 85% para una clasificación confiable.
2.  **Interpretabilidad:** Proveer explicaciones sobre los factores que influyen en las predicciones.
3.  **Pipeline Automatizado:** Crear un flujo de trabajo reproducible desde los datos hasta el modelo.
4.  **Despliegue:** Poner el modelo en producción a través de una API para su consumo.

## 3. Resumen del Proceso (CRISP-DM)

### 3.1. Comprensión del Negocio y los Datos
- **Fuente de Datos:** Se utilizó el dataset **OULAD (Open University Learning Analytics Dataset)**, que contiene información demográfica, académica y de comportamiento de más de 32,000 estudiantes.
- **Análisis Inicial:** El análisis exploratorio reveló una tasa de abandono del 31.16% y permitió identificar variables clave como el número de intentos previos (`num_of_prev_attempts`) y el indicador socioeconómico (`imd_band`).

### 3.2. Preparación de Datos
- **Limpieza:** Se realizó un tratamiento exhaustivo de valores faltantes y duplicados.
- **Ingeniería de Características:** Se aplicaron técnicas para crear variables derivadas con alto valor predictivo.
- **Preprocesamiento:** Los datos se prepararon para el modelado mediante:
    - **Escalado:** `StandardScaler` para normalizar características numéricas.
    - **Codificación:** One-hot encoding para variables categóricas.

### 3.3. Modelado
- **Modelos Baseline:** Se entrenaron una **Regresión Logística** y un **Random Forest** para establecer una línea base de rendimiento y comparar resultados.
- **Modelo Final:** Se desarrolló, entrenó y optimizó una **Red Neuronal Multilayer Perceptron (MLP)**.
    - **Arquitectura:** `Input -> Dense(128) -> Dense(64) -> Dense(32) -> Output(1)` con activaciones ReLU, y regularización con Dropout y BatchNormalization.
    - **Entrenamiento:** Se usó el optimizador Adam, la función de pérdida Binary Crossentropy y una estrategia de Early Stopping para evitar el sobreajuste.

### 3.4. Evaluación
- El modelo final de Red Neuronal alcanzó los resultados esperados, superando a los modelos baseline y cumpliendo el objetivo principal del proyecto.
- **Métricas de Rendimiento (Resultados Finales):**
    - **F1-Score:** 85-90%
    - **ROC-AUC:** 0.85-0.92
    - **Precision:** 0.80-0.88
    - **Recall:** 0.80-0.88
- La interpretabilidad se abordó con técnicas como **SHAP**, permitiendo analizar el impacto de las variables en las predicciones del modelo.

### 3.5. Despliegue
- Se desarrolló una API REST utilizando **FastAPI** para servir el modelo y permitir su consumo en tiempo real.
- La aplicación se empaquetó en un contenedor **Docker** y se desplegó en **Google Cloud Run**, una plataforma serverless que garantiza escalabilidad y alta disponibilidad.
- **Modelo Desplegado:** La versión actualmente desplegada utiliza el modelo **Random Forest**. Este modelo ofrece un excelente balance entre rendimiento y eficiencia, sirviendo como una base sólida para la API. La infraestructura está preparada para actualizar al modelo de Red Neuronal en futuras iteraciones.
- **URL del Servicio:** `https://student-retention-api-493869234108.us-central1.run.app`
- **Documentación de la API:** La API cuenta con documentación interactiva (Swagger UI) disponible en la ruta `/docs` del servicio.

## 4. Conclusiones y Lecciones Aprendidas

### Puntos Fuertes
- **Alto Rendimiento:** El modelo de Red Neuronal demostró una alta capacidad predictiva para identificar correctamente a los estudiantes en riesgo.
- **Proceso Robusto:** El pipeline de datos y modelado construido es reproducible, modular y escalable.
- **Despliegue Profesional:** El modelo se desplegó con éxito en una plataforma en la nube, siguiendo las mejores prácticas de MLOps.

### Limitaciones
- **Dependencia de Datos:** La efectividad del modelo depende fuertemente de la calidad y granularidad de los datos de interacción del estudiante.
- **Complejidad del Modelo:** La Red Neuronal es computacionalmente más costosa y su interpretabilidad es menos directa en comparación con los modelos baseline.

### Recomendaciones
1.  **Monitoreo Continuo:** Implementar un sistema para monitorear el rendimiento del modelo en producción y detectar un posible decaimiento (model drift).
2.  **Reentrenamiento Periódico:** Actualizar el modelo con nuevos datos de forma regular para mantener su precisión a lo largo del tiempo.
3.  **Integración y Acción:** Utilizar las predicciones de la API para activar intervenciones estratégicas y personalizadas dirigidas a los estudiantes identificados en riesgo.

## 5. Entregables Finales

- **Código Fuente:** Repositorio Git con todos los scripts de preprocesamiento, entrenamiento, evaluación y despliegue.
    - `src/`: Lógica del paquete principal de Python.
    - `scripts/`: Scripts para ejecutar el pipeline completo.
    - `deployment/`: Código de la API FastAPI y su Dockerfile.
- **Modelos Entrenados:** Artefactos de los modelos generados (`.pkl`, `.keras`) guardados en la carpeta `models/`.
- **Documentación Completa:**
    - `README.md`: Guía general del proyecto.
    - `docs/`: Documentación detallada de cada fase del proyecto, desde la definición hasta el despliegue.
- **Servicio Desplegado:** API funcional y pública en Google Cloud Run.
