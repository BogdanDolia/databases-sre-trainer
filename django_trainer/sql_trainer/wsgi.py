"""
WSGI config for sql_trainer project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sql_trainer.settings')

application = get_wsgi_application()