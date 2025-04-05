#!/bin/bash
set -e

# Make sure we have the right packages installed
pip uninstall -y django-codemirror2 django-ace || true
pip install --no-cache-dir markdown>=3.5.0

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping for 1 second"
  sleep 1
done
echo "PostgreSQL is up and running!"

# Create migrations directory if it doesn't exist
mkdir -p /app/sql_trainer/lessons/migrations
touch /app/sql_trainer/lessons/migrations/__init__.py

# Make migrations and apply them
echo "Creating migrations..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if not exists (will be skipped if user already exists)
python manage.py createsuperuser --noinput || true

# Import lessons from fixture if available
echo "Importing lessons from fixtures..."
if [ -f /app/fixtures/lessons.json ]; then
  python manage.py import_lessons --clear
  echo "Lessons imported successfully!"
else
  echo "No lesson fixtures found. You can create lessons through the admin interface."
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000