import pandas as pd
import json
import requests
import time
from sklearn.metrics import accuracy_score, classification_report

# --- Configuración ---
API_URL = "https://student-retention-api-493869234108.us-central1.run.app/predict"
NUM_SAMPLES_PER_CLASS = 50

def run_balanced_batch_test():
    """
    Ejecuta una prueba por lotes contra la API desplegada, utilizando
    una muestra balanceada de ambas clases (abandono y no abandono).
    """
    print(f"🚀 Iniciando prueba por lotes con una muestra balanceada ({NUM_SAMPLES_PER_CLASS} de cada clase)...")

    # --- 1. Cargar Datos y Crear Muestra Balanceada ---
    try:
        # Cargar información de características
        with open('data/processed/feature_info.json', 'r') as f:
            feature_info = json.load(f)
            numeric_cols = feature_info['numerical_columns']

        # Cargar datasets completos
        features_df = pd.read_csv('data/processed/modeling_features.csv', header=0)
        target_df = pd.read_csv('data/processed/modeling_target.csv', header=0)
        
        # Unir para facilitar el muestreo
        full_df = pd.concat([features_df, target_df], axis=1)
        target_col = target_df.columns[0]

        # Separar por clases
        df_class_0 = full_df[full_df[target_col] == 0]
        df_class_1 = full_df[full_df[target_col] == 1]

        # Tomar muestras aleatorias
        sample_class_0 = df_class_0.sample(n=NUM_SAMPLES_PER_CLASS, random_state=42)
        sample_class_1 = df_class_1.sample(n=NUM_SAMPLES_PER_CLASS, random_state=42)

        # Combinar y barajar la muestra de prueba
        test_df = pd.concat([sample_class_0, sample_class_1]).sample(frac=1, random_state=42).reset_index(drop=True)
        
        features_subset = test_df[features_df.columns.difference([target_col])]
        target_subset = test_df[[target_col]]

        print(f"✅ Muestra de prueba balanceada creada con {len(test_df)} registros.")

    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Error al preparar los datos: {e}. Asegúrate de que los archivos existan y haya suficientes muestras de cada clase.")
        return

    # --- 2. Iterar y Llamar a la API ---
    predictions = []
    actual_values = []

    for index, row in features_subset.iterrows():
        y_true = target_subset.iloc[index].values[0]
        actual_values.append(y_true)

        features_series = row[numeric_cols].fillna(0)
        features_list = [float(x) for x in features_series.tolist()]
        payload = {"features": features_list}

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            y_pred = result.get('prediction')
            predictions.append(y_pred)

            status = "✅ Coincide" if y_true == y_pred else f"❌ No coincide (Real: {y_true}, Pred: {y_pred})"
            print(f"Registro #{index + 1}: {status}")

        except requests.exceptions.RequestException as e:
            print(f"Registro #{index + 1}: 🚨 Error en la llamada a la API: {e}")
            predictions.append(None)
        
        time.sleep(0.1)

    # --- 3. Calcular y Mostrar Resultados ---
    valid_indices = [i for i, p in enumerate(predictions) if p is not None]
    valid_predictions = [predictions[i] for i in valid_indices]
    valid_actuals = [actual_values[i] for i in valid_indices]

    if len(valid_predictions) > 0:
        accuracy = accuracy_score(valid_actuals, valid_predictions)
        report = classification_report(valid_actuals, valid_predictions)
        
        print("\n--- Resultados del Lote Balanceado ---")
        print(f"Total de registros probados: {len(features_subset)}")
        print(f"Llamadas exitosas a la API: {len(valid_predictions)}")
        print(f"Precisión (Accuracy): {accuracy:.2%}\n")
        print("Reporte de Clasificación Detallado:")
        print(report)
        print("------------------------------------")
    else:
        print("\nNo se pudieron obtener predicciones válidas.")

if __name__ == "__main__":
    run_balanced_batch_test() 