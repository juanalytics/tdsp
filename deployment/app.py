import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
# from tensorflow import keras # Desactivado temporalmente

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Predicción de Retención Estudiantil")

# --- Carga de Modelo y Scaler ---
# MODEL_PATH = 'models/neural_network_model.keras'
SCALER_PATH = 'models/neural_network_model_scaler.pkl'

model = None
scaler = None
model_loaded = False
try:
    # model = keras.models.load_model(MODEL_PATH) # Desactivado
    scaler_data = joblib.load(SCALER_PATH)
    scaler = scaler_data['scaler']
    model_loaded = True # Forzamos a true para probar
except Exception as e:
    model_loaded = False
    print(f"Error loading assets: {e}")


# --- Definición del payload de entrada ---
class StudentFeatures(BaseModel):
    features: List[float]

# --- Endpoints de la API ---
@app.get("/", summary="Endpoint raíz para verificar estado")
def read_root():
    """Verifica que la API esté funcionando."""
    return {"status": "ok", "model_loaded": model_loaded}

@app.post("/predict", summary="Realizar una predicción")
def predict(student: StudentFeatures):
    """
    Recibe las características de un estudiante y predice si abandonará.
    """
    if not model_loaded or not scaler:
        return {"error": "Modelo o scaler no cargado."}

    # Devolvemos una predicción falsa
    return {
        "prediction": 0,
        "probability": 0.1
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 