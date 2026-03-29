#!/bin/sh
set -e
python manage.py migrate --noinput
python setup_tenants.py
exec daphne -b 0.0.0.0 -p ${PORT:-8000} pyservice.asgi:application
