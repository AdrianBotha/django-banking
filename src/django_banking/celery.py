import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_banking.settings')

app = Celery('django_banking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
