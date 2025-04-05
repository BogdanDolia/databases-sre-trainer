from django.core.management.base import BaseCommand
from sql_trainer.lessons.models import Lesson, Exercise, UserProgress

class Command(BaseCommand):
    help = 'Clear all lessons, exercises, and user progress from the database'

    def handle(self, *args, **options):
        # Delete all user progress first (to avoid foreign key constraints)
        progress_count = UserProgress.objects.count()
        UserProgress.objects.all().delete()
        
        # Delete all exercises
        exercise_count = Exercise.objects.count()
        Exercise.objects.all().delete()
        
        # Delete all lessons
        lesson_count = Lesson.objects.count()
        Lesson.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {lesson_count} lessons, {exercise_count} exercises, and {progress_count} progress records.'))