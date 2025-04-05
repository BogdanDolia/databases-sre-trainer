# PostgreSQL SRE Trainer - SQL and Database Management Training Platform

An interactive web application for learning PostgreSQL, SQL commands, and database management concepts for Site Reliability Engineers.

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

## Setup Instructions

For detailed setup instructions, see [DOCKER_README.md](DOCKER_README.md).

## Changes Made

The following enhancements have been implemented in this version:

1. **Fixed Database Connection Issues:**
   - Added PostgreSQL client to the Django Docker image
   - Enhanced entrypoint script with database connection health check
   - Improved migrations handling

2. **Enhanced Lesson User Interface:**
   - Integrated SQL query editor directly on the lesson page
   - Added dynamic exercise loading to improve user experience
   - Improved feedback for query execution

3. **Extended SQL Functionality:**
   - Enabled support for all SQL commands (previously limited to SELECT queries)
   - Added proper handling for non-SELECT queries
   - Enhanced result display for different query types

4. **Expanded Lessons and Exercises:**
   - Added multiple lessons covering basic SQL, advanced queries, and database management
   - Created various exercises with real-world examples
   - Implemented option to start with an empty database or initialize with sample data

5. **UI/UX Improvements:**
   - Added clear error messages and query results
   - Implemented interactive exercise selection
   - Added real-time feedback for completed exercises
   - Added database management buttons for admins

6. **Database Management Features:**
   - Start with empty database for pure learning experience
   - Reset database button to clear all tables and start over
   - Initialize database option to load sample data when needed
   - Admin-only access to database management functions

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