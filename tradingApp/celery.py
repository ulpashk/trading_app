import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tradingApp.settings")

app = Celery("tradingApp")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.task
def debug_task():
    print("Celery is working!")