#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for Postgres to be ready (simple check)
# In a real prod environment, we might use a robust wait-for-it script, 
# but this works for compose.
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (CSS/JS)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
# We use 0.0.0.0 to allow access from outside the container
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000