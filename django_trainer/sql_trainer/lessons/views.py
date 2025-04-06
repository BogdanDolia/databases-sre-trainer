import json
import subprocess
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection, connections
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Lesson, Exercise, UserProgress
from .forms import QueryForm
from .sql_scripts import DROP_USER_TABLES, DROP_USER_VIEWS

def index(request):
    """View function for home page of site."""
    lessons = Lesson.objects.all().order_by('order')
    
    # Get progress if user is authenticated
    completed_lessons = set()
    completed_exercises = set()
    
    if request.user.is_authenticated:
        progress = UserProgress.objects.filter(user=request.user, completed=True)
        completed_exercises = set(p.exercise_id for p in progress if p.exercise)
        
        # Check which lessons have all exercises completed
        for lesson in lessons:
            lesson_exercises = lesson.exercises.all()
            if lesson_exercises.count() > 0:  # Only consider lessons with exercises
                lesson_exercise_ids = set(ex.id for ex in lesson_exercises)
                completed_lesson_exercise_ids = set(p.exercise_id for p in progress 
                                                  if p.exercise and p.lesson_id == lesson.id)
                
                # If all exercises for this lesson are completed, mark the lesson as completed
                if lesson_exercise_ids.issubset(completed_lesson_exercise_ids):
                    completed_lessons.add(lesson.id)
    
    context = {
        'lessons': lessons,
        'completed_lessons': completed_lessons,
        'completed_exercises': completed_exercises,
    }
    
    return render(request, 'lessons/index.html', context)

def lesson_detail(request, slug):
    """View function for lesson detail page."""
    lesson = get_object_or_404(Lesson, slug=slug)
    exercises = lesson.exercises.all().order_by('order')
    
    # Get progress if user is authenticated
    if request.user.is_authenticated:
        progress_completed = UserProgress.objects.filter(
            user=request.user, 
            lesson=lesson,
            completed=True
        )
        completed_exercises = set(p.exercise_id for p in progress_completed)
        
        # Get all progress records to restore last solutions
        all_progress = UserProgress.objects.filter(
            user=request.user,
            lesson=lesson
        )
        # Create dictionary of exercise_id -> last_solution
        exercise_solutions = {p.exercise_id: p.last_solution for p in all_progress if p.last_solution}
        
        # Check if all exercises for this lesson are completed
        lesson_completed = False
        if exercises.count() > 0:  # Only consider lessons with exercises
            lesson_exercise_ids = set(ex.id for ex in exercises)
            if lesson_exercise_ids.issubset(completed_exercises):
                lesson_completed = True
    else:
        completed_exercises = set()
        exercise_solutions = {}
        lesson_completed = False
    
    context = {
        'lesson': lesson,
        'exercises': exercises,
        'completed_exercises': completed_exercises,
        'exercise_solutions': exercise_solutions,
        'lesson_completed': lesson_completed,
    }
    
    return render(request, 'lessons/lesson_detail.html', context)

def exercise_detail(request, lesson_slug, exercise_id):
    """View function for exercise detail page."""
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    exercise = get_object_or_404(Exercise, id=exercise_id, lesson=lesson)
    
    # Get user progress for this exercise (if user is authenticated)
    if request.user.is_authenticated:
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            exercise=exercise,
            defaults={'completed': False}
        )
        
        # Check if all exercises for this lesson are completed
        all_exercises = lesson.exercises.all()
        progress_completed = UserProgress.objects.filter(
            user=request.user,
            lesson=lesson,
            completed=True
        )
        completed_exercises = set(p.exercise_id for p in progress_completed)
        
        lesson_completed = False
        if all_exercises.count() > 0:
            lesson_exercise_ids = set(ex.id for ex in all_exercises)
            if lesson_exercise_ids.issubset(completed_exercises):
                lesson_completed = True
    else:
        # For non-authenticated users, create a dummy progress object
        from types import SimpleNamespace
        progress = SimpleNamespace(completed=False, last_solution='')
        lesson_completed = False
    
    # Get initial query from either user's last solution or the exercise default
    initial_query = progress.last_solution if progress.last_solution else exercise.initial_query
    form = QueryForm(initial_query=initial_query)
    
    # ENHANCED DEBUG - print detailed information
    print(f"====================== EXERCISE DEBUG INFO ======================")
    print(f"Exercise ID: {exercise.id}")
    print(f"Exercise Title: {exercise.title}")
    print(f"Instruction (Length: {len(exercise.instruction)}): {repr(exercise.instruction)}")
    print(f"Hints (Length: {len(exercise.hints)}): {repr(exercise.hints)}")
    print(f"Initial Query (Length: {len(exercise.initial_query)}): {repr(exercise.initial_query)}")
    print(f"================================================================")
    
    # Create a fresh context with explicit strings for debugging
    context = {
        'lesson': lesson,
        'exercise': exercise,
        'form': form,
        'progress': progress,
        'instruction_text': str(exercise.instruction),
        'hints_text': str(exercise.hints),
        'lesson_completed': lesson_completed if request.user.is_authenticated else False,
    }
    
    return render(request, 'lessons/exercise_detail.html', context)

def execute_query(request):
    """API endpoint to execute SQL queries."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        query = data.get('query', '')
        exercise_id = data.get('exercise_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)
    
    # Execute the query - allow all types of SQL commands
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            # For SELECT queries, return the results
            if query.strip().lower().startswith('select'):
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            # For non-SELECT queries (CREATE, INSERT, UPDATE, DELETE, etc.)
            else:
                # Get the number of affected rows
                affected_rows = cursor.rowcount
                columns = ["message"]
                rows = [{"message": f"Query executed successfully. Affected rows: {affected_rows}"}]
        
        # If exercise_id is provided, check if the query matches the solution
        is_correct = False
        if exercise_id:
            try:
                exercise = Exercise.objects.get(id=exercise_id)
                
                # Normalize and compare queries (simple comparison for now)
                user_query = ' '.join(query.lower().split())
                solution_query = ' '.join(exercise.solution_query.lower().split())
                
                # Check if the queries are equivalent
                # This is a simple check - in a production app, you might want to compare query plans
                if user_query == solution_query:
                    is_correct = True
                
                # If user is authenticated, save progress
                if request.user.is_authenticated:
                    # Save the user's solution
                    progress, created = UserProgress.objects.get_or_create(
                        user=request.user,
                        lesson=exercise.lesson,
                        exercise=exercise,
                        defaults={'last_solution': query}
                    )
                    
                    if not created:
                        progress.last_solution = query
                    
                    if is_correct:
                        progress.completed = True
                        progress.completed_at = timezone.now()
                    
                    progress.save()
                    
                    # Check if all exercises for this lesson are now completed
                    lesson_completed = False
                    if is_correct:
                        all_exercises = exercise.lesson.exercises.all()
                        if all_exercises.count() > 0:
                            lesson_exercise_ids = set(ex.id for ex in all_exercises)
                            
                            # Get all completed exercises after saving this one
                            progress_completed = UserProgress.objects.filter(
                                user=request.user,
                                lesson=exercise.lesson,
                                completed=True
                            )
                            completed_exercise_ids = set(p.exercise_id for p in progress_completed)
                            
                            # Check if all exercises are completed
                            if lesson_exercise_ids.issubset(completed_exercise_ids):
                                lesson_completed = True
                
            except Exercise.DoesNotExist:
                pass
        
        # Add lesson_completed value to the response if it exists
        response_data = {
            'columns': columns,
            'rows': rows,
            'is_correct': is_correct
        }
        
        # Add lesson_completed flag if it's been computed
        if 'lesson_completed' in locals() and lesson_completed:
            response_data['lesson_completed'] = lesson_completed
            
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def sandbox(request):
    """SQL sandbox view for free-form querying."""
    form = QueryForm()
    
    context = {
        'form': form,
        'is_sandbox': True
    }
    
    return render(request, 'lessons/sandbox.html', context)

def reset_database(request):
    """Reset the database to an empty state."""
    if request.method == 'POST':
        try:
            # Drop all tables (without dropping the database) to reset
            with connection.cursor() as cursor:
                # First remove all user progress if user is authenticated
                if request.user.is_authenticated:
                    UserProgress.objects.filter(user=request.user).delete()
                
                # Drop all tables that may have been created during exercises
                cursor.execute(DROP_USER_TABLES)
                
                # Also drop any views, functions, etc.
                cursor.execute(DROP_USER_VIEWS)
                
            messages.success(request, "Database has been reset successfully. All tables have been cleared.")
        except Exception as e:
            messages.error(request, f"Error resetting database: {str(e)}")
        
        return redirect('lessons:index')
    
    return render(request, 'lessons/reset_confirm.html')

def initialize_database(request):
    """Initialize the database with sample data (without lessons)."""
    if request.method == 'POST':
        try:
            # Find the initialization script
            possible_paths = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'db_init', '01-init.sql'),
                '/app/db_init/01-init.sql',
                '/db_init/01-init.sql'
            ]
            db_init_path = next((p for p in possible_paths if os.path.exists(p)), possible_paths[0])
            
            # Execute the SQL script using psql
            with connection.cursor() as cursor:
                with open(db_init_path, 'r') as f:
                    sql_script = f.read()
                    cursor.execute(sql_script)
            
            messages.success(request, "Database has been initialized with sample tables and data. You can now add lessons manually.")
        except Exception as e:
            messages.error(request, f"Error initializing database: {str(e)}")
        
        return redirect('lessons:index')
    
    return render(request, 'lessons/initialize_confirm.html')