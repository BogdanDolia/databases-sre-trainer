# PostgreSQL SRE Trainer

This application is an interactive SQL trainer for learning PostgreSQL and database management concepts for Site Reliability Engineers.

## Features

- Interactive SQL lessons with exercises
- SQL query editor with real-time execution against a PostgreSQL database
- Support for various SQL commands including SELECT, CREATE TABLE, INSERT, UPDATE, DELETE, etc.
- Exercises with automated validation
- SQL sandbox for free-form experimentation
- Empty initial database with admin controls to initialize or reset
- Database management tools for admins to control the learning environment

## Technical Overview

This project consists of:

1. A Django web application
2. A PostgreSQL database
3. Docker Compose for easy deployment

## Running the Application

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

3. The Django application will be available at http://localhost:8000
4. Login to the admin interface at http://localhost:8000/admin (username: admin, password: admin)

### Stopping the Application

```bash
docker-compose down
```

To remove all data including the database volume:

```bash
docker-compose down -v
```

## Project Structure

- `django_trainer/`: Django application code
  - `sql_trainer/`: Main Django project
  - `sql_trainer/lessons/`: App for SQL lessons and exercises
  - `entrypoint.sh`: Startup script for the Django container
- `docker-compose.yml`: Docker Compose configuration

## Project Components

### PostgreSQL Database

- **Database Name**: sql_trainer
- **Username**: postgres
- **Password**: postgres
- **Port**: 5432 (accessible from host system)

The database starts empty by default. Administrators can initialize it with sample data through the web interface.

### Django Web Application

The Django application provides:
- Interactive SQL query interface with syntax highlighting
- Comprehensive lessons on SQL and database management
- Hands-on exercises with automatic validation
- SQL sandbox for free-form experimentation

## Running Custom SQL

You can connect to the database directly using any PostgreSQL client:

```bash
# Using psql from Docker
docker exec -it postgres_db psql -U postgres -d sql_trainer

# From your host machine
psql -h localhost -p 5432 -U postgres -d sql_trainer
```

## Recent Changes

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

## Notes for Development

- The `debug_lessons.py` script can be used to check database connectivity and create sample lessons
- Any database changes made in the sandbox persist within the Docker container's lifetime
- Static files are collected automatically during startup

## Troubleshooting

- **Database Connection Issues**: Check if the PostgreSQL container is running (`docker ps`)
- **Web Application Not Loading**: View logs with `docker-compose logs django_app`
- **Database Initialization Errors**: Check logs with `docker-compose logs database`

## Database Connection Settings

The application uses the following environment variables for database connection:

- `DATABASE_HOST`: database
- `DATABASE_NAME`: sql_trainer
- `DATABASE_USER`: postgres
- `DATABASE_PASSWORD`: postgres
- `DATABASE_PORT`: 5432

These are configured in the Docker Compose file and passed to the Django application.