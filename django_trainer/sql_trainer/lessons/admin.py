from django.contrib import admin
from .models import Lesson, Exercise, UserProgress

class ExerciseInline(admin.StackedInline):
    model = Exercise
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'order')
        }),
        ('Exercise Content', {
            'fields': ('instruction', 'hints'),
            'classes': ('collapse',)
        }),
        ('SQL', {
            'fields': ('initial_query', 'solution_query'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    list_filter = ()
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExerciseInline]
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'order')
        }),
        ('Content', {
            'fields': ('description', 'content'),
            'classes': ('wide',)
        }),
    )

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order')
    list_filter = ('lesson',)
    search_fields = ('title', 'instruction')
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('lesson', 'title', 'order')
        }),
        ('Exercise Content', {
            'fields': ('instruction', 'hints'),
            'classes': ('wide',)
        }),
        ('SQL', {
            'fields': ('initial_query', 'solution_query'),
            'classes': ('wide',)
        }),
    )

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'exercise', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at', 'lesson')
    search_fields = ('user__username', 'lesson__title', 'exercise__title')