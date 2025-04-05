FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client for health checks
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Don't install codemirror2
RUN pip uninstall -y django-codemirror2 || true

# Copy project files
COPY . .

# Create initial migrations directory to ensure it exists
RUN mkdir -p /app/sql_trainer/lessons/migrations
RUN touch /app/sql_trainer/lessons/migrations/__init__.py

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Use entrypoint script
CMD ["./entrypoint.sh"]