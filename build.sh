#!/usr/bin/env bash
# Script de build para Render.
# Se configura como "Build Command" en el servicio: bash build.sh

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
