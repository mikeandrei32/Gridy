#!/bin/bash
set -e

# Run database migrations on container launch
if [[ "$*" == *"runserver"* ]] || [[ "$*" == *"gunicorn"* ]]; then
    echo "Running Database Migrations..."
    python manage.py migrate --noinput
fi

echo "Starting Server: $@"
exec "$@"