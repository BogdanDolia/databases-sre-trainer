#!/bin/bash
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if not exists (will be skipped if user already exists)
python manage.py createsuperuser --noinput || true

# Import lessons
echo "Importing lessons from SQL and Markdown files..."
python seed_lessons.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000