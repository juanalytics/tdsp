# Diccionario de Datos - Dataset OULAD

## Descripción General

Este diccionario describe todas las variables presentes en los archivos del dataset Open University Learning Analytics Dataset (OULAD). Cada variable está documentada con su tipo de dato, descripción, valores posibles y relevancia para el análisis de retención estudiantil.

---

## 1. Archivo: `courses.csv`

### Variables del curso

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `code_module` | String | Código identificador del módulo/curso | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** - Diferentes cursos pueden tener diferentes tasas de abandono |
| `code_presentation` | String | Código de la presentación del curso (año y semestre) | 2013J, 2014J, 2013B, 2014B | **Alta** - Permite análisis temporal y por cohorte |
| `module_presentation_length` | Integer | Duración del módulo en días | 234-269 días | **Media** - Cursos más largos pueden tener mayor riesgo de abandono |

---

## 2. Archivo: `studentInfo.csv`

### Variables demográficas y académicas

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `code_module` | String | Código del módulo (ver courses.csv) | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** |
| `code_presentation` | String | Código de presentación (ver courses.csv) | 2013J, 2014J, 2013B, 2014B | **Alta** |
| `id_student` | Integer | Identificador único del estudiante | 11391-272000+ | **Alta** - Variable clave para joins |
| `gender` | String | Género del estudiante | M (Male), F (Female) | **Media** - Puede influir en patrones de comportamiento |
| `region` | String | Región geográfica del estudiante | East Anglian Region, Scotland, North Western Region, South East Region, West Midlands Region, Wales, North Region, South Region, London Region, Yorkshire Region, East Midlands Region, South West Region, Ireland, North Ireland | **Media** - Diferencias regionales en acceso y comportamiento |
| `highest_education` | String | Nivel educativo más alto alcanzado | HE Qualification, A Level or Equivalent, Lower Than A Level, Post Graduate Qualification, No Formal quals | **Alta** - Indicador de preparación académica |
| `imd_band` | String | Banda del Índice de Deprivación Múltiple (socioeconómico) | 90-100%, 80-90%, 70-80%, 60-70%, 50-60%, 40-50%, 30-40%, 20-30%, 10-20%, 0-10%, "" (vacío) | **Alta** - Indicador socioeconómico importante |
| `age_band` | String | Banda de edad del estudiante | 0-35, 35-55, 55<= | **Media** - Diferentes grupos de edad pueden tener diferentes patrones |
| `num_of_prev_attempts` | Integer | Número de intentos previos en el módulo | 0, 1, 2, 3, 4, 5, 6 | **Alta** - Indicador fuerte de riesgo de abandono |
| `studied_credits` | Integer | Número de créditos estudiados | 60, 90, 120, 240 | **Media** - Carga académica |
| `disability` | String | Si el estudiante tiene alguna discapacidad | Y (Yes), N (No) | **Media** - Puede requerir apoyo adicional |
| `final_result` | String | Resultado final del estudiante en el módulo | Pass, Withdrawn, Fail, Distinction | **Alta** - Variable objetivo para predicción |

---

## 3. Archivo: `studentRegistration.csv`

### Variables de registro

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `code_module` | String | Código del módulo | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** |
| `code_presentation` | String | Código de presentación | 2013J, 2014J, 2013B, 2014B | **Alta** |
| `id_student` | Integer | Identificador del estudiante | 11391-272000+ | **Alta** |
| `date_registration` | Integer | Día de registro (relativo al inicio del curso) | Valores negativos (antes del inicio) | **Alta** - Registro temprano puede indicar compromiso |
| `date_unregistration` | Integer | Día de desregistro (relativo al inicio del curso) | Valores positivos o vacío | **Alta** - Indicador directo de abandono |

---

## 4. Archivo: `assessments.csv`

### Variables de evaluaciones

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `code_module` | String | Código del módulo | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** |
| `code_presentation` | String | Código de presentación | 2013J, 2014J, 2013B, 2014B | **Alta** |
| `id_assessment` | Integer | Identificador único de la evaluación | 1752-1760+ | **Alta** |
| `assessment_type` | String | Tipo de evaluación | TMA (Tutor Marked Assignment), Exam, CMA (Computer Marked Assignment) | **Media** - Diferentes tipos pueden tener diferentes patrones |
| `date` | Integer | Día de la evaluación (relativo al inicio del curso) | 19, 54, 117, 166, 215, "" (vacío para exámenes) | **Alta** - Timing de evaluaciones |
| `weight` | Integer | Peso de la evaluación en la calificación final | 10, 20, 30, 100 | **Media** - Importancia de la evaluación |

---

## 5. Archivo: `studentAssessment.csv`

### Variables de resultados de evaluaciones

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `id_assessment` | Integer | Identificador de la evaluación (ver assessments.csv) | 1752-1760+ | **Alta** |
| `id_student` | Integer | Identificador del estudiante | 11391-272000+ | **Alta** |
| `date_submitted` | Integer | Día de entrega (relativo al inicio del curso) | 17, 18, 22, 26, etc. | **Alta** - Puntualidad en entregas |
| `is_banked` | Integer | Si la evaluación fue "banked" (guardada para uso futuro) | 0, 1 | **Baja** - Información administrativa |
| `score` | Integer | Calificación obtenida en la evaluación | 0-100 | **Alta** - Rendimiento académico directo |

---

## 6. Archivo: `vle.csv`

### Variables del entorno virtual de aprendizaje

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `id_site` | Integer | Identificador único del sitio/recurso | 546943, 546712, etc. | **Media** |
| `code_module` | String | Código del módulo | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** |
| `code_presentation` | String | Código de presentación | 2013J, 2014J, 2013B, 2014B | **Alta** |
| `activity_type` | String | Tipo de actividad en el VLE | resource, oucontent, url, homepage, forumng, glossary, subpage, quiz, page, externalquiz, ouwiki, dataplus, folder, repeatactivity, htmlactivity, elluminate, questionnaire, sharedsubpage, oucollaborate, oustudio, urlresource, dualpane, page, notebook, repeatactivity, ouelluminate, oucollaborate, oustudio, urlresource, dualpane, page, notebook | **Alta** - Diferentes tipos de interacción |
| `week_from` | Integer | Semana de inicio de disponibilidad | Valores enteros o vacío | **Media** - Timing de recursos |
| `week_to` | Integer | Semana de fin de disponibilidad | Valores enteros o vacío | **Media** - Timing de recursos |

---

## 7. Archivo: `studentVle.csv`

### Variables de interacciones estudiantiles

| Variable | Tipo | Descripción | Valores Posibles | Relevancia |
|----------|------|-------------|------------------|------------|
| `code_module` | String | Código del módulo | AAA, BBB, CCC, DDD, EEE, FFF, GGG | **Alta** |
| `code_presentation` | String | Código de presentación | 2013J, 2014J, 2013B, 2014B | **Alta** |
| `id_student` | Integer | Identificador del estudiante | 11391-272000+ | **Alta** |
| `id_site` | Integer | Identificador del sitio (ver vle.csv) | 546943, 546712, etc. | **Media** |
| `date` | Integer | Día de la interacción (relativo al inicio del curso) | -10, -9, -8, ..., 269 | **Alta** - Patrones temporales de comportamiento |
| `sum_click` | Integer | Número total de clics en esa actividad en esa fecha | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269 | **Alta** - Intensidad de participación |

---

## Variables Clave para Predicción de Abandono

### **Variables de Alto Riesgo:**
1. **`num_of_prev_attempts`** - Estudiantes con múltiples intentos previos
2. **`final_result`** - Variable objetivo (Withdrawn = abandono)
3. **`date_unregistration`** - Fecha de desregistro
4. **`imd_band`** - Indicador socioeconómico
5. **`highest_education`** - Nivel educativo previo

### **Variables de Comportamiento:**
1. **`sum_click`** - Intensidad de participación en la plataforma
2. **`date`** (en studentVle) - Patrones temporales de actividad
3. **`date_submitted`** - Puntualidad en entregas
4. **`score`** - Rendimiento académico

### **Variables Demográficas:**
1. **`age_band`** - Grupo de edad
2. **`gender`** - Género
3. **`region`** - Región geográfica
4. **`disability`** - Necesidades especiales

---

## Notas Importantes

- **Fechas relativas:** Todas las fechas están en días relativos al inicio del curso (día 0)
- **Valores faltantes:** Algunas variables como `imd_band` pueden tener valores vacíos
- **Anonimización:** Todos los datos están anonimizados para proteger la privacidad
- **Integridad referencial:** Las variables `id_student`, `code_module`, y `code_presentation` permiten joins entre tablas

