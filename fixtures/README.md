# Lesson Management

This directory contains JSON fixture files that define the lessons and exercises for the SQL Trainer application.

## Managing Lessons

### Importing Lessons
Lessons will be automatically imported from `lessons.json` when the application starts. 
To use this feature, rename `sample_lessons.json` to `lessons.json` or create your own file.

### Creating Lessons Manually
You have two options for creating lessons:

**Option 1: Admin Interface**
1. Log in to the admin interface (http://localhost:8000/admin/) 
2. Go to the Lessons section
3. Click "Add Lesson" to create a new lesson
4. Add exercises to your lesson

**Option 2: Sample Lessons Command**
Run the provided command to create sample lessons with exercises:

```bash
docker exec django_trainer python manage.py create_sample_lessons
```

### Exporting Lessons
After creating lessons, you can export them to a fixture file:

```bash
docker exec django_trainer python manage.py export_lessons
```

This will create a JSON file at `/app/fixtures/lessons.json` that you can copy to your host:

```bash
docker cp django_trainer:/app/fixtures/lessons.json ./fixtures/
```

Now you can commit this file to your repository for version control.

### Importing Custom Lessons
To import lessons from a custom file:

```bash
docker exec django_trainer python manage.py import_lessons --input=/app/fixtures/my_custom_lessons.json --clear
```

## Lesson Format

The lesson fixture file is a JSON array containing lesson and exercise objects:

```json
[
  {
    "model": "lessons.lesson",
    "pk": 1,
    "fields": {
      "title": "Lesson Title",
      "slug": "lesson-slug",
      "description": "Brief description",
      "content": "HTML content",
      "order": 1
    }
  },
  {
    "model": "lessons.exercise",
    "pk": 1,
    "fields": {
      "lesson": 1,
      "title": "Exercise Title",
      "instruction": "Exercise instructions",
      "hints": "Hints for the exercise",
      "initial_query": "Initial SQL query",
      "solution_query": "Solution SQL query",
      "order": 1
    }
  }
]
```

The content field in lessons supports HTML, allowing you to format your lessons with headings, code blocks, lists, etc.