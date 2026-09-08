#!/bin/bash
set -e

# Only execute migrations when launching the Daphne backend, not Celery workers
if [[ "$*" == *"daphne"* ]] || [[ "$*" == *"runserver"* ]]; then
    echo "Running Database Migrations..."
    python manage.py migrate --noinput
fi

echo "Starting Server: $@"
exec "$@"