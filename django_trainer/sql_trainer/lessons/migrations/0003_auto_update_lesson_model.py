from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_update_field_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='hints',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={},
        ),
        migrations.AlterModelOptions(
            name='exercise',
            options={},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='updated_at',
        ),
    ]