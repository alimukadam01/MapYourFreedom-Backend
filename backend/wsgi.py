"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Adjust these paths
project_home = '/home/mapyourfreedom/public_html/backend.mapyourfreedom.com/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
