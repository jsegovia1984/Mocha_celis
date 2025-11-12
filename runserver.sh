#!/bin/bash

# =======================================================
# SCRIPT PARA INICIAR EL SERVIDOR DJANGO EN EL PUERTO 8080
# =======================================================

echo "=========================================="
echo "🚀 Iniciando el servidor de Django..."
echo "Puerto: 8080 (http://127.0.0.1:8080/)"
echo "=========================================="

# Ejecuta el servidor en la IP 0.0.0.0 (accesible desde cualquier interfaz)
# y en el puerto 8080.

python manage.py runserver 0.0.0.0:8080

# El script terminará cuando se detenga el servidor (Ctrl+C)
echo ""
echo "🛑 Servidor detenido."