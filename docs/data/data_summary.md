# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos (EDA) del dataset OULAD.

## Resumen general de los datos

A continuación se presenta un resumen general de los archivos principales:

| Archivo                | Registros   | Columnas | Memoria   | Valores faltantes | Duplicados |
|------------------------|------------:|---------:|----------:|------------------:|-----------:|
| student_info           |     32,593  |      12  |   16.3 MB |            1,111  |          0 |
| courses                |         22  |       3  |   0.00 MB |                0  |          0 |
| assessments            |        206  |       6  |   0.04 MB |               11  |          0 |
| student_assessments    |    173,912  |       5  |   6.63 MB |              173  |          0 |
| student_registration   |     32,593  |       5  |   4.04 MB |           22,566  |          0 |
| vle                    |      6,364  |       6  |   1.13 MB |           10,486  |          0 |
| student_vle            | 10,655,280  |       6  | 1402.31 MB|                0  |    787,170 |

## Resumen de calidad de los datos

- **Valores faltantes:**
  - `student_info`: 1,111 valores faltantes (3.41%)
  - `assessments`: 11 valores faltantes (5.34%)
  - `student_registration`: 22,566 valores faltantes (principalmente en `date_unregistration`)
  - `vle`: 10,486 valores faltantes
- **Duplicados:**
  - `student_vle`: 787,170 filas duplicadas (posibles múltiples interacciones en el mismo recurso/fecha)
- **Tipos incorrectos:**
  - Algunos campos como fechas y pesos pueden estar como string en vez de numérico.
- **Acciones tomadas:**
  - Validación de integridad referencial (todas las relaciones clave están correctas)
  - Identificación de valores faltantes y duplicados para su tratamiento en el preprocesamiento

## Variable objetivo

La variable objetivo es `final_result` en `student_info`.

- **Distribución:**
  - Pass: 12,361 (38%)
  - Withdrawn: 10,156 (31%)
  - Fail: 7,052 (22%)
  - Distinction: 3,024 (9%)
- **Tasa de abandono:** 31.16% (Withdrawn)

## Variables individuales

Ejemplo de variables en `student_info`:

- `gender`: M (17,875), F (14,718)
- `region`: 13 regiones distintas
- `highest_education`: 5 niveles educativos
- `imd_band`: 10 bandas socioeconómicas + vacío
- `age_band`: 3 grupos de edad
- `num_of_prev_attempts`: 0 a 6
- `studied_credits`: 60, 90, 120, 240
- `disability`: Y/N

Variables numéricas y categóricas han sido identificadas para análisis y modelado.

## Ranking de variables

Variables más relevantes para predecir abandono (según teoría y distribución):

1. `num_of_prev_attempts` (número de intentos previos)
2. `imd_band` (banda socioeconómica)
3. `highest_education` (nivel educativo previo)
4. `age_band` (grupo de edad)
5. `sum_click` (interacciones en la plataforma)
6. `date_unregistration` (fecha de desmatrícula)
7. `score` (calificaciones en evaluaciones)

## Relación entre variables explicativas y variable objetivo

- **Tasa de abandono** varía según región, edad, nivel educativo y actividad en la plataforma.
- **Correlación positiva** entre mayor número de intentos previos y probabilidad de abandono.
- **Menor actividad** (`sum_click`) y menor rendimiento (`score`) se asocian a mayor abandono.
- **Distribución de género**: similar tasa de abandono entre M y F.

Se recomienda profundizar con visualizaciones y análisis estadístico en el notebook de EDA.
