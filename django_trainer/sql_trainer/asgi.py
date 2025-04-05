"""
ASGI config for sql_trainer project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sql_trainer.settings')

application = get_asgi_application()