#!/bin/bash

# =======================================================
# SCRIPT DE MIGRACIÓN RÁPIDA PARA DJANGO
# Proyecto: mocha_celis
# App principal: datos_personales
# =======================================================

# 1. Nombre de la aplicación a migrar (puedes cambiarlo o pasarlo como argumento)
APP_NAME="datos_personales"

# Función para manejar errores
handle_error() {
  echo ""
  echo "❌ ERROR: Falló el comando anterior. Deteniendo la migración."
  echo "Por favor, revisa el mensaje de error."
  exit 1
}

echo "=========================================="
echo "🚀 Iniciando proceso de migración para ${APP_NAME}..."
echo "=========================================="

# 2. Eliminar migraciones anteriores de la aplicación (excepto __init__.py)
echo "🧹 Limpiando migraciones antiguas en ${APP_NAME}/migrations/..."
find "${APP_NAME}/migrations" -type f -not -name "__init__.py" -delete
# Navega al directorio donde están tus apps
# cd mocha_celis/

# Elimina migraciones de datos_personales
find datos_personales/migrations -type f -not -name "__init__.py" -delete
echo "Migraciones de datos_personales limpiadas."

# Elimina migraciones de Acompanamiento
find Acompanamiento/migrations -type f -not -name "__init__.py" -delete
echo "Migraciones de Acompanamiento limpiadas."

# Elimina migraciones de InsercionLaboral
find InsercionLaboral/migrations -type f -not -name "__init__.py" -delete
echo "Migraciones de InsercionLaboral limpiadas."
if [ $? -ne 0 ]; then
  handle_error
fi
echo "✅ Limpieza completa."


# 3. Crear el nuevo archivo de migración
echo ""
echo "📝 Creando nuevos archivos de migración..."
python manage.py makemigrations "${APP_NAME}"

if [ $? -ne 0 ]; then
  handle_error
fi
echo "✅ Archivos de migración generados."

# 4. Aplicar todas las migraciones
echo ""
echo "🛠️ Aplicando todas las migraciones a la base de datos..."
python manage.py migrate

if [ $? -ne 0 ]; then
  handle_error
fi
echo "✅ Migraciones aplicadas con éxito."

echo ""
echo "=========================================="
echo "✨ Proceso de migración rápido finalizado."
echo "=========================================="
