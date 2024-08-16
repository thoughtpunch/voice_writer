# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
import multiprocessing
from billiard import context
from celery import Celery

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

# Set the start method to 'spawn'
multiprocessing.set_start_method('spawn', force=True)

# Set the start method to 'spawn' for the billiard context
context._force_start_method("spawn")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('voice_writer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set up Redis as the broker using the REDIS_URL environment variable.
app.conf.broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
