#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Collect static files
echo "Collect static files"
python manage.py collectstatic -c --noinput

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 WeissWurstTool.wsgi