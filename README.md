# PostgreSQL SRE Trainer - SQL and Database Management Training Platform

An interactive web application for learning PostgreSQL, SQL commands, and database management concepts for Site Reliability Engineers.

## Running Locally for Learning SQL

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone this repository)

### Starting the Application

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd databases-sre-trainer
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. The application will be available at http://localhost:8000
4. Login to the admin interface at http://localhost:8000/admin (username: admin, password: admin)

### Stopping the Application

```bash
docker-compose down
```

To remove all data including the database volume:

```bash
docker-compose down -v
```

### Connecting to the Database Directly

You can connect to the database directly using any PostgreSQL client:

```bash
# Using psql from Docker
docker exec -it postgres_db psql -U postgres -d sql_trainer

# From your host machine
psql -h localhost -p 5432 -U postgres -d sql_trainer
```

## Project Overview

This application provides a comprehensive platform for learning SQL and database management through interactive lessons and exercises. It allows users to execute SQL queries against a real PostgreSQL database and receive immediate feedback.

## Features

- **Interactive SQL Lessons**: Learn SQL concepts through structured lessons
- **Integrated SQL Editor**: Write and execute SQL queries directly in the browser
- **Full SQL Support**: Execute any SQL command including SELECT, CREATE TABLE, INSERT, UPDATE, DELETE, etc.
- **Exercise Validation**: Get immediate feedback on exercise solutions
- **SQL Sandbox**: Experiment freely with SQL commands in a safe environment
- **Empty Initial Database**: Start with a clean database to build from scratch
- **Database Management**: Reset database to clear all tables or initialize with sample data
- **Lesson Management**: Easy lesson import/export using JSON fixtures

## Technical Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL 14
- **Containerization**: Docker and Docker Compose
- **Frontend**: Bootstrap 5, JavaScript

## Project Structure

- `django_trainer/`: Django application code
  - `sql_trainer/`: Main Django project
  - `sql_trainer/lessons/`: App for SQL lessons and exercises
  - `entrypoint.sh`: Startup script for the Django container
- `docker-compose.yml`: Docker Compose configuration

## Running the Application

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up -d
```

Then access the application at http://localhost:8000.

## Lesson Management

Lessons can be managed in multiple ways:

1. **Using Fixtures**: Place a `lessons.json` file in the `/fixtures` directory, and lessons will be automatically imported when the application starts.

2. **Admin Interface**: Create and manage lessons through the admin interface.

3. **Sample Lessons Command**: Create sample lessons automatically:
   ```bash
   docker exec django_trainer python manage.py create_sample_lessons
   ```

To export lessons for version control:

```bash
docker exec django_trainer python manage.py export_lessons
docker cp django_trainer:/app/fixtures/lessons.json ./fixtures/
```

For more details, see the [Lesson Management README](fixtures/README.md).

## Admin Access

- URL: http://localhost:8000/admin
- Username: admin
- Password: admin

## Database Connection Settings

The application uses the following environment variables for database connection:

- `DATABASE_HOST`: database
- `DATABASE_NAME`: sql_trainer
- `DATABASE_USER`: postgres
- `DATABASE_PASSWORD`: postgres
- `DATABASE_PORT`: 5432

## Troubleshooting

- **Database Connection Issues**: Check if the PostgreSQL container is running (`docker ps`)
- **Web Application Not Loading**: View logs with `docker-compose logs django_app`
- **Database Initialization Errors**: Check logs with `docker-compose logs database`
