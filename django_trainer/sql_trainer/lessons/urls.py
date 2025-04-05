from django.urls import path
from . import views
from django.http import JsonResponse
from .models import Exercise

app_name = 'lessons'

# Debug view
def debug_exercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id)
        return JsonResponse({
            'id': exercise.id,
            'title': exercise.title,
            'instruction': exercise.instruction,
            'hints': exercise.hints
        })
    except Exercise.DoesNotExist:
        return JsonResponse({'error': 'Exercise not found'}, status=404)

urlpatterns = [
    path('', views.index, name='index'),
    path('sandbox/', views.sandbox, name='sandbox'),
    path('execute-query/', views.execute_query, name='execute_query'),
    path('reset-database/', views.reset_database, name='reset_database'),
    path('initialize-database/', views.initialize_database, name='initialize_database'),
    path('debug-exercise/<int:exercise_id>/', debug_exercise, name='debug_exercise'),
    path('<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:lesson_slug>/exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]