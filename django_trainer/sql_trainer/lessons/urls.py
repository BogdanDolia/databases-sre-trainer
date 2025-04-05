from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.index, name='index'),
    path('sandbox/', views.sandbox, name='sandbox'),
    path('execute-query/', views.execute_query, name='execute_query'),
    path('reset-database/', views.reset_database, name='reset_database'),
    path('initialize-database/', views.initialize_database, name='initialize_database'),
    path('<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:lesson_slug>/exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]