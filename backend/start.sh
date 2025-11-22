#!/bin/bash
# This script is for Unix/Linux/Mac systems
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn chemviz.wsgi:application --bind 0.0.0.0:${PORT:-8000}

