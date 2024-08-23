# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
import multiprocessing
from billiard import context
from celery import Celery

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_START_METHOD = os.getenv('CELERY_START_METHOD', 'fork')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Set the start method for the multiprocessing either 'spawn' or 'fork'
multiprocessing.set_start_method(CELERY_START_METHOD, force=True)
context._force_start_method(CELERY_START_METHOD)

app = Celery('voice_writer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set up Redis as the broker using the REDIS_URL environment variable.
app.conf.broker_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
