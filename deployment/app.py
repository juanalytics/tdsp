import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import numpy as np
import json

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Predicción de Retención Estudiantil")

# --- Carga de Artefactos ---
MODEL_PATH = 'models/random_forest_model.pkl'
FEATURES_PATH = 'feature_info.json'

pipeline = None
model_loaded = False
numerical_features = []

try:
    # Cargar el pipeline completo
    pipeline = joblib.load(MODEL_PATH)
    
    # Cargar la lista de características numéricas
    with open(FEATURES_PATH, 'r') as f:
        feature_info = json.load(f)
        numerical_features = feature_info.get('numerical_columns', [])
    
    if pipeline and numerical_features:
        model_loaded = True
    else:
        print("Error: No se pudo cargar el pipeline o las características.")
        model_loaded = False
except Exception as e:
    print(f"Error loading artifacts: {e}")
    model_loaded = False

# --- Definición del payload de entrada ---
class StudentFeatures(BaseModel):
    # La lista debe tener la misma longitud que numerical_features
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
    if not model_loaded:
        return {"error": "Modelo o características no cargados."}

    if len(student.features) != len(numerical_features):
        return {
            "error": f"Se esperaban {len(numerical_features)} características, pero se recibieron {len(student.features)}."
        }

    # Crear DataFrame solo con las características numéricas y sus nombres correctos
    features_df = pd.DataFrame([student.features], columns=numerical_features)
    
    # Predecir
    try:
        prediction = pipeline.predict(features_df)[0]
        prediction_proba = pipeline.predict_proba(features_df)[0][1] # Probabilidad de la clase 1
    except Exception as e:
        return {"error": f"Error durante la predicción: {e}"}


    return {
        "prediction": int(prediction),
        "probability": float(prediction_proba)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 