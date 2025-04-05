from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Import lessons and exercises from a fixture file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input',
            default='/app/fixtures/lessons.json',
            help='Input fixture file path',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing lessons before import',
        )

    def handle(self, *args, **options):
        input_path = options['input']
        clear_existing = options['clear']
        
        # Clear existing lessons if requested
        if clear_existing:
            self.stdout.write('Clearing existing lessons...')
            call_command('clear_lessons')
            
        # Import lessons from fixture
        try:
            call_command('loaddata', input_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported lessons from {input_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing lessons: {str(e)}'))
            return