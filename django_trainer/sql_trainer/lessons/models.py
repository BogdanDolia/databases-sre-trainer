from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    """Model representing a lesson."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    content = models.TextField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Exercise(models.Model):
    """Model representing an exercise within a lesson."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    instruction = models.TextField()
    hints = models.TextField(blank=True)
    initial_query = models.TextField(blank=True)
    solution_query = models.TextField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

class UserProgress(models.Model):
    """Model representing a user's progress."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_solution = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'lesson', 'exercise']
    
    def __str__(self):
        if self.exercise:
            return f"{self.user.username} - {self.lesson.title} - {self.exercise.title}"
        return f"{self.user.username} - {self.lesson.title}"