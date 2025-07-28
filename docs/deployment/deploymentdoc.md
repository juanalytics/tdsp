# Documentación de Despliegue del Modelo

Este documento detalla la infraestructura, el código y el proceso utilizados para desplegar el modelo de predicción de retención estudiantil en Google Cloud Platform, siguiendo la estructura requerida.

---

## Infraestructura

- **Nombre del modelo:** `student-retention-api` (Nombre del servicio en Google Cloud Run)
- **Plataforma de despliegue:** Google Cloud Run
- **Requisitos técnicos:**
  - Python 3.9
  - Docker
  - Google Cloud SDK (`gcloud` CLI)
  - **Librerías Principales:** FastAPI, Uvicorn, Scikit-learn, Pandas.
- **Requisitos de seguridad:**
  - El servicio en Cloud Run está configurado para permitir acceso público no autenticado (`--allow-unauthenticated`) para fines de demostración.
  - Todo el tráfico es servido a través de HTTPS, gestionado automáticamente por Google Cloud Run.
- **Diagrama de arquitectura:**

    ```mermaid
    graph TD
        subgraph "Usuario"
            U[Cliente HTTP]
        end
    
        subgraph "Google Cloud Platform"
            CR[Google Cloud Run]
            GCR[Google Container Registry]
        end
    
        subgraph "Contenedor Docker"
            F[Aplicación FastAPI]
            M[Pipeline del Modelo .pkl]
            J[feature_info.json]
        end
    
        U --"HTTPS Request<br/>(e.g., /predict)"--> CR
        CR --"Extrae imagen para servir"--> GCR
        CR --"Ejecuta Contenedor"--> F
        F --"Carga"--> M
        F --"Carga"--> J
        F --"Devuelve Predicción (JSON)"--> U
    ```

---

## Código de despliegue

- **Archivo principal:** `deployment/app.py`
- **Rutas de acceso a los archivos:**
  - `deployment/app.py`: Aplicación principal de la API FastAPI.
  - `deployment/Dockerfile`: Definición del contenedor Docker.
  - `deployment/requirements.txt`: Dependencias de Python para la API.
  - `models/random_forest_model.pkl`: Pipeline del modelo entrenado (Imputador + Escalador + Modelo).
  - `data/processed/feature_info.json`: Metadatos con la lista de características numéricas que espera el modelo.
  - `scripts/test_api_call.py`: Script para ejecutar pruebas por lotes contra la API desplegada.
- **Variables de entorno:**
  - `PORT`: Proporcionada automáticamente por Cloud Run para indicar en qué puerto debe escuchar la aplicación. El código está preparado para usarla.

---

## Documentación del despliegue

### Instrucciones de instalación y configuración

Este proceso combina la configuración del entorno local y de Google Cloud con la instalación (despliegue) del servicio.

**Paso 1: Configurar el Entorno Local y de GCP**

1. **Iniciar sesión en gcloud:** Autentica tu cuenta y selecciona el proyecto.

    ```bash
    gcloud init
    ```

2. **Habilitar las APIs necesarias:** Activa las APIs de Cloud Run y Container Registry.

    ```bash
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    ```

3. **Configurar Docker:** Autoriza a Docker para que pueda interactuar con el registro de contenedores de tu proyecto.

    ```bash
    gcloud auth configure-docker
    ```

**Paso 2: Instalación (Despliegue del Modelo)**

1. **Construir la Imagen Docker:** Desde la raíz del proyecto, ejecuta el siguiente comando. La bandera `--platform` es crucial para evitar errores de arquitectura (ej. en Mac M1/M2). Reemplaza `[PROJECT_ID]` y `[VERSION]`.

    ```bash
    docker build --platform linux/amd64 -t gcr.io/[PROJECT_ID]/student-retention-api:[VERSION] -f deployment/Dockerfile .
    ```

2. **Subir la Imagen a GCR:** Publica la imagen construida en el registro de contenedores de Google.

    ```bash
    docker push gcr.io/[PROJECT_ID]/student-retention-api:[VERSION]
    ```

3. **Desplegar en Cloud Run:** Crea o actualiza el servicio en Cloud Run con la nueva imagen.

    ```bash
    gcloud run deploy student-retention-api \
      --image gcr.io/[PROJECT_ID]/student-retention-api:[VERSION] \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
    ```

### Instrucciones de uso

La API desplegada expone dos endpoints principales. La URL base del servicio es: `https://student-retention-api-493869234108.us-central1.run.app`

**GET /**

- **Descripción:** Verifica el estado de la API.
- **Comando de Ejemplo:**

    ```bash
    curl https://student-retention-api-493869234108.us-central1.run.app
    ```

- **Respuesta Esperada:**

    ```json
    {"status":"ok","model_loaded":true}
    ```

**POST /predict**

- **Descripción:** Realiza una predicción de abandono estudiantil.
- **Payload (Cuerpo de la Petición):** Un objeto JSON con una clave `features`, que es una lista de **24 valores numéricos (flotantes o enteros)**.
- **Comando de Ejemplo:**

    ```bash
    curl -X POST "https://student-retention-api-493869234108.us-central1.run.app/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [240.0, -159.0, 268.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 10.0, 0.0, 0.0, 1.0, -23.0]}'
    ```

- **Respuesta Esperada:**

    ```json
    {"prediction":0,"probability":0.42}
    ```

    *(Nota: La probabilidad puede variar, pero la estructura será la misma).*

**Documentación Interactiva (Swagger UI)**

- Se puede acceder a una interfaz interactiva para realizar pruebas en: `https://student-retention-api-493869234108.us-central1.run.app/docs`

### Instrucciones de mantenimiento

- **Actualizar el Servicio:** Para desplegar una nueva versión del modelo o de la API, simplemente repita el **Paso 2 de Instalación** con una nueva etiqueta de versión (ej. `v9`). Cloud Run gestionará la transición del tráfico sin tiempo de inactividad.
- **Ver Logs:** Los logs del contenedor se pueden visualizar en la consola de Google Cloud, en la sección "Cloud Logging", para diagnosticar cualquier problema.
- **Troubleshooting Común:**
  - **Arquitectura:** Si la construcción de la imagen se realiza en un Mac con chip Apple Silicon (ARM), es crucial usar la bandera `--platform linux/amd64` para asegurar la compatibilidad con Cloud Run.
  - **Timeout:** El error "container failed to start and listen on port" usualmente significa que la aplicación no está usando la variable de entorno `PORT` que Cloud Run le asigna.
  - **Input Incorrecto:** La API devolverá un error si el número de características en la lista `features` no es exactamente 24.
