# Generated by Django 4.2.20 on 2025-04-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_update_lesson_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
