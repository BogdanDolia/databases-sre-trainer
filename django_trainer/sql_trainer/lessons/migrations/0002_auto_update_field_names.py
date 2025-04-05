from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='description',
            new_name='instruction',
        ),
    ]