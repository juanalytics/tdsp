import mlflow
import os
import shutil
from pathlib import Path

def promote_best_model():
    """
    Encuentra el mejor modelo de Random Forest en los experimentos de MLflow
    y lo copia a la carpeta de despliegue.
    """
    print("🚀 Iniciando promoción del mejor modelo...")

    # Configuración
    EXPERIMENT_NAME = "Baseline Models"
    MODEL_NAME = "random_forest"
    METRIC_TO_OPTIMIZE = "metrics.cv_cv_f1_mean" # Usamos la métrica de validación cruzada
    DESTINATION_PATH = Path(__file__).parent.parent.parent / "models"
    DESTINATION_FILE = DESTINATION_PATH / "promoted_model.pkl"

    # Crear directorio de destino si no existe
    DESTINATION_PATH.mkdir(parents=True, exist_ok=True)

    try:
        # Obtener el experimento
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if not experiment:
            print(f"❌ Error: El experimento '{EXPERIMENT_NAME}' no fue encontrado.")
            return

        # Buscar el mejor run para el modelo específico
        best_run = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string=f"tags.mlflow.runName = '{MODEL_NAME}'",
            order_by=[f"{METRIC_TO_OPTIMIZE} DESC"],
            max_results=1
        ).iloc[0]

        run_id = best_run.run_id
        best_metric_value = best_run[METRIC_TO_OPTIMIZE]
        
        print(f"✅ Mejor run encontrado para '{MODEL_NAME}':")
        print(f"  - Run ID: {run_id}")
        print(f"  - F1-Score (CV Mean): {best_metric_value:.4f}")

        # Descargar el artefacto del modelo
        client = mlflow.tracking.MlflowClient()
        local_path = client.download_artifacts(run_id, MODEL_NAME)
        
        # El modelo sklearn se guarda en una carpeta, el archivo es 'model.pkl'
        model_file_path = Path(local_path) / "model.pkl"

        if not model_file_path.exists():
            print(f"❌ Error: No se encontró 'model.pkl' en los artefactos del run {run_id}.")
            return

        # Copiar y renombrar el modelo a la carpeta de destino
        shutil.copy(model_file_path, DESTINATION_FILE)
        
        print(f"✅ Modelo promocionado y copiado a: {DESTINATION_FILE}")

    except IndexError:
        print(f"❌ Error: No se encontraron runs para el modelo '{MODEL_NAME}' en el experimento '{EXPERIMENT_NAME}'.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    promote_best_model() 