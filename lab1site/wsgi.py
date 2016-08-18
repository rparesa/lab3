"""
WSGI config for lab1site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab1site.settings")

os.environ["AWS_ACCESS_KEY_ID"] = 'AKIAIPTKNTVT2B2YDFFQ'
os.environ["AWS_SECRET_ACCESS_KEY"] = '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'

application = get_wsgi_application()
