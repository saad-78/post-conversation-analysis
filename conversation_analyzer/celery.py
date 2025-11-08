import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conversation_analyzer.settings')

app = Celery('conversation_analyzer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'analyze-new-conversations-daily': {
        'task': 'analysis.tasks.analyze_all_new_conversations',
        'schedule': crontab(hour=0, minute=0), 
    },
}

app.conf.timezone = 'UTC'
