"""SQL Trainer URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/lessons/', permanent=False)),
    path('lessons/', include('sql_trainer.lessons.urls')),
]