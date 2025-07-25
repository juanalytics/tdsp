# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY deployment/requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación y el modelo
# NOTA: La estructura de directorios debe coincidir
COPY deployment/app.py .
COPY models/ ./models/
COPY data/processed/feature_info.json .

# Exponer el puerto que usará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación
# El host 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
CMD ["python", "app.py"] 