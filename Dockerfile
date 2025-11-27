# Usar una imagen base oficial de Python (ligera)
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y bufferice la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# --- BLOQUE NUEVO PARA SSL ---
# 1. Instalar herramientas de certificados
RUN apt-get update && apt-get install -y ca-certificates

# 2. Copiar tu certificado Fortinet a la carpeta del sistema
# Asegúrate de que "Fortinet.crt" esté en la misma carpeta que este Dockerfile
COPY Fortinet.crt /usr/local/share/ca-certificates/Fortinet.crt

# 3. Actualizar el almacén de certificados del sistema
RUN update-ca-certificates

# 4. Decirle a Python/Requests que use los certificados del sistema
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# -----------------------------

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Exponer el puerto
EXPOSE 8000

# Comando por defecto (puede ser sobreescrito por docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]