import os

from django.conf import settings

from celery import Celery


"""App settings for celery"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "check.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
