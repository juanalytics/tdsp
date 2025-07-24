import pytest
import requests
import os

# Obtener la URL de la API desde una variable de entorno o usar un valor por defecto
API_URL = os.environ.get("API_URL", "https://student-retention-api-493869234108.us-central1.run.app")

def test_root_endpoint():
    """Prueba que el endpoint raíz '/' esté funcionando."""
    response = requests.get(API_URL)
    
    # Verificar que la respuesta sea exitosa (código 200)
    assert response.status_code == 200
    
    # Verificar el contenido de la respuesta
    json_response = response.json()
    assert json_response["status"] == "ok"
    # En la versión actual de prueba, model_loaded es true
    assert json_response["model_loaded"] is True

def test_predict_endpoint_success():
    """Prueba que el endpoint '/predict' funcione con datos válidos."""
    # Datos de ejemplo. El número de características debe coincidir con el esperado por el modelo.
    # Usamos 24, que es el número de columnas numéricas.
    payload = {
        "features": [0.5, 1.2, -0.8, 2.1, 0.0, -1.5, 0.3, 1.8, -0.9, 0.1] * 2 + [0.1, 0.2, 0.3, 0.4]
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    
    # Verificar que la respuesta sea exitosa
    assert response.status_code == 200
    
    # Verificar el contenido de la respuesta
    json_response = response.json()
    assert "prediction" in json_response
    assert "probability" in json_response
    # Para la versión actual de prueba, la predicción está hardcodeada
    assert json_response["prediction"] == 0
    assert json_response["probability"] == 0.1

def test_predict_endpoint_invalid_data():
    """Prueba que el endpoint '/predict' falle con datos inválidos."""
    # Payload con un tipo de dato incorrecto (string en lugar de float)
    payload = {
        "features": ["not-a-float"]
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    
    # FastAPI debería devolver un error 422 Unprocessable Entity
    assert response.status_code == 422 