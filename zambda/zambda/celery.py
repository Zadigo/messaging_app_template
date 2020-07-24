import os

from celery import Celery
from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zambda.settings')

# app = Celery('zambda')

# app.config_from_object('django.conf:settings', namespace='CELERY')

app = Celery(
    'zambda',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    include=[
        'forum.tasks'
    ]
)


app.conf.beat_schedule = {
    'custom_task': {
        'task': 'custom_task',
        # 'schedule': crontab(second='*/30'),
        'schedule': 30.0,
        'args': ('What'),
    }
}

app.conf.timezone = 'UTC'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, custom_periodic_task.s('hello'), name='Custom Periodic Task')

@app.task
def custom_task(name):
    print(f'This is what is done {name}')

@app.task
def custom_periodic_task(name):
    print(f'This is what is done {name}')

