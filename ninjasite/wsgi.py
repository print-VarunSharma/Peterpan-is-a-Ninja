"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
# from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ninjasite.settings")

application = get_wsgi_application()
# application = DjangoWhiteNoise(application)
