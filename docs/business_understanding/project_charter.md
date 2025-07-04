# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

[DeepRetention – Modelo Predictivo de Retención Estudiantil con Deep Learning]

## Objetivo del Proyecto

## 📌 **Objetivo del Proyecto**

El objetivo principal de este proyecto es desarrollar y desplegar un modelo predictivo basado en redes neuronales, utilizando el conjunto de datos abierto **Open University Learning Analytics Dataset (OULAD)**, para identificar oportunamente estudiantes con alto riesgo de abandono en cursos virtuales. A través del análisis profundo y automatizado de variables demográficas, comportamentales y académicas recopiladas semanalmente, el modelo permitirá detectar patrones tempranos que anticipen la deserción estudiantil.

Este proyecto es particularmente importante debido al crecimiento exponencial de la educación en línea, donde la falta de contacto directo hace difícil monitorear la motivación y el compromiso de los estudiantes. La capacidad de predecir de manera precisa y temprana la deserción permitirá a las instituciones educativas implementar estrategias de intervención personalizadas, optimizar sus recursos educativos, reducir costos operativos y, sobre todo, mejorar significativamente las tasas de retención estudiantil.

Adicionalmente, el modelo será diseñado bajo principios metodológicos ágiles, lo que garantizará su adaptabilidad y escalabilidad en diferentes contextos educativos, cursos y plataformas tecnológicas, convirtiéndose así en una herramienta valiosa no solo desde el punto de vista académico sino también administrativo y estratégico.


## Alcance del Proyecto

### Incluye:

#### Descripción de los datos disponibles:
- **Información demográfica y académica anonimizada** de 32.593 estudiantes, incluyendo variables como edad, género, nivel educativo previo, y estado socioeconómico, así como el detalle de asignaturas matriculadas y finalizadas.
- **Registros detallados de interacciones semanales** con la plataforma virtual, consistentes en aproximadamente 10,6 millones de eventos clasificados en clics, accesos a materiales educativos, descargas de contenido, visualización de videos y participación en foros, proporcionando una visión granular del comportamiento del estudiante.
- **Datos de desempeño académico**, incluyendo calificaciones obtenidas en evaluaciones parciales y finales, puntualidad en la entrega de actividades, frecuencia y consistencia en la participación activa dentro del curso.

#### Descripción de los resultados esperados:
- **Desarrollo de un modelo predictivo robusto basado en redes neuronales**, particularmente modelos tipo MLP (Multi-Layer Perceptron) o CNN-1D (Convolutional Neural Network de una dimensión), capaz de clasificar eficazmente (con un F1-score ≥ 85%) el riesgo de abandono estudiantil en etapas tempranas del curso.
- **Generación de un informe técnico exhaustivo** que incluya métricas clave de desempeño como precisión, recall, F1-score y área bajo la curva ROC (Receiver Operating Characteristic).
- **Identificación y explicación clara de las variables críticas** que influyen significativamente en el abandono estudiantil mediante técnicas avanzadas de interpretación como análisis SHAP (SHapley Additive exPlanations) o importancia por permutación, que permitan sustentar decisiones pedagógicas y administrativas fundamentadas.

#### Criterios de éxito del proyecto:
- Alcanzar una métrica de desempeño de clasificación, medida por **F1-score, igual o superior al 85%**, demostrando capacidad predictiva sólida y confiable.
- Implementar un **pipeline automatizado, reproducible y escalable** para la carga, limpieza, procesamiento y análisis exploratorio inicial de los datos, garantizando su aplicabilidad futura en diversos contextos educativos.
- Proporcionar un **notebook en Jupyter (o similar) con código perfectamente documentado, claro, estructurado, reproducible**, y listo para ser utilizado como base en futuras iteraciones del proyecto o en adaptaciones a otros contextos educativos.

### Excluye:
- Análisis o predicciones que permitan identificar individualmente a los estudiantes debido a **restricciones éticas y de privacidad**, asegurando siempre la confidencialidad y anonimato de los participantes.
- Implementación o evaluación de intervenciones educativas específicas o **acompañamiento psicológico posterior** a la identificación del riesgo de abandono estudiantil.
- Incorporación de información externa o enriquecimiento adicional que **no esté directamente provisto por el conjunto de datos OULAD**, manteniendo así la consistencia metodológica y la integridad del análisis.

## Metodología

El proyecto seguirá una metodología ágil basada en el marco CRISP-DM adaptado a Scrum, dividiendo el proceso en iteraciones breves (sprints) claramente definidas. En cada sprint se realizarán tareas específicas de carga y exploración inicial de los datos, limpieza y preprocesamiento, creación de características relevantes, entrenamiento de modelos (red neuronal MLP o CNN-1D), y evaluación continua de resultados según métricas preestablecidas (F1-score, precisión, recall, ROC-AUC). Se utilizarán herramientas de control de versiones y notebooks documentados para asegurar la transparencia y reproducibilidad del proceso. Adicionalmente, se aplicarán técnicas modernas de interpretación de modelos (SHAP o importancia por permutación) para validar y explicar las variables que más impactan en la predicción. Esto permitirá ajustar continuamente el modelo basado en retroalimentación iterativa hasta alcanzar los criterios de éxito definidos.

## Cronograma

| Semana | Etapa                                           | Actividades Clave                                                                 |
|--------|--------------------------------------------------|------------------------------------------------------------------------------------|
| Semana 1<br>(1–7 de julio) | Entendimiento del negocio y carga de datos         | - Revisión del problema y objetivo del modelo<br>- Lectura y comprensión del dataset OULAD<br>- Carga, inspección inicial y auditoría de calidad de los datos |
| Semana 2<br>(8–14 de julio) | Preprocesamiento y análisis exploratorio de datos  | - Limpieza y normalización de variables<br>- Creación de variables relevantes<br>- Análisis estadístico y visual de comportamientos y correlaciones |
| Semana 3<br>(15–21 de julio) | Modelado y entrenamiento de la red neuronal        | - Definición de arquitectura (MLP o CNN-1D)<br>- Entrenamiento y ajuste de hiperparámetros<br>- Validación cruzada y comparación con baseline |
| Semana 4<br>(22–28 de julio) | Evaluación, interpretación y entrega final         | - Análisis de métricas (F1, ROC-AUC, precision, recall)<br>- Interpretación del modelo (SHAP o permutaciones)<br>- Redacción del informe final y entrega del notebook |

## Equipo del Proyecto

- **Juan Manuel Pérez** – Líder del proyecto / Responsable técnico de modelado y entrega final.
- **Xamir Ernesto Rojas** – Analista de datos / Encargado de la carga, preprocesamiento y visualización de datos.

## Presupuesto

Este proyecto se desarrolla en el marco de un diplomado académico, por lo que no cuenta con una asignación presupuestaria monetaria directa. Sin embargo, se estima el siguiente uso de recursos no financieros:

- **Infraestructura computacional:** uso de plataformas gratuitas como Google Colab (GPU T4 de acceso limitado), Jupyter Notebooks y almacenamiento en Google Drive.
- **Herramientas de desarrollo:** bibliotecas de código abierto (NumPy, Pandas, Scikit-learn, TensorFlow/Keras, Matplotlib, SHAP, entre otras).
- **Fuentes de datos:** dataset OULAD (Open University Learning Analytics Dataset), de acceso abierto y licencia académica sin costo.
- **Tiempo estimado de dedicación:** entre 25 y 35 horas hombre por integrante, distribuidas a lo largo de las 4 semanas del proyecto.

Dado que todos los recursos son de libre acceso o están disponibles sin costo para estudiantes, el presupuesto efectivo del proyecto es **cero (0)** pesos, sin comprometer la calidad técnica ni la reproducibilidad del trabajo.


## Stakeholders

- **Stakeholders del proyecto:**
  - *Docente del diplomado* – Supervisor académico del proyecto.
  - *Institución educativa virtual (simulada)* – Usuario potencial del modelo predictivo.
  - *Equipo del proyecto* – Desarrolladores responsables de la ejecución técnica y entrega del modelo.

- **Relación con los stakeholders:**
  - El docente actúa como guía metodológica, evalúa entregables y valida el cumplimiento de criterios técnicos y pedagógicos.
  - La institución educativa virtual (rol simulado) representa el entorno de aplicación, sirviendo como referencia para los requerimientos funcionales del modelo.
  - El equipo del proyecto mantiene comunicación directa con el docente y orienta su trabajo hacia la solución de una problemática realista, basada en datos reales y contexto académico.

- **Expectativas de los stakeholders:**
  - Recibir un modelo predictivo funcional, documentado y validado, que permita identificar con alta precisión a los estudiantes en riesgo de abandono.
  - Obtener un análisis interpretativo que explique las variables clave asociadas a la deserción.
  - Contar con un entregable reproducible, claro y útil para futuras adaptaciones o implementaciones en escenarios educativos reales.

