from django.core.management.base import BaseCommand
import json
from sql_trainer.lessons.models import Lesson, Exercise

class Command(BaseCommand):
    help = 'Export all lessons and exercises to a JSON fixture file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='/app/fixtures/lessons.json',
            help='Output file path',
        )

    def handle(self, *args, **options):
        output_path = options['output']
        
        # Collect all lessons and exercises
        lessons_data = []
        exercises_data = []
        
        for lesson in Lesson.objects.all().order_by('order'):
            lesson_data = {
                "model": "lessons.lesson",
                "pk": lesson.id,
                "fields": {
                    "title": lesson.title,
                    "slug": lesson.slug,
                    "description": lesson.description,
                    "content": lesson.content,
                    "order": lesson.order
                }
            }
            lessons_data.append(lesson_data)
            
            for exercise in Exercise.objects.filter(lesson=lesson).order_by('order'):
                exercise_data = {
                    "model": "lessons.exercise",
                    "pk": exercise.id,
                    "fields": {
                        "lesson": exercise.lesson.id,
                        "title": exercise.title,
                        "instruction": exercise.instruction,
                        "hints": exercise.hints,
                        "initial_query": exercise.initial_query,
                        "solution_query": exercise.solution_query,
                        "order": exercise.order
                    }
                }
                exercises_data.append(exercise_data)
        
        # Combine data and write to file
        fixture_data = lessons_data + exercises_data
        
        with open(output_path, 'w') as f:
            json.dump(fixture_data, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully exported {len(lessons_data)} lessons and {len(exercises_data)} exercises to {output_path}'
        ))