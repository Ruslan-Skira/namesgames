# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# from django.conf import settings
#
# from celery.schedules import crontab
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'namesgames.settings')
#
# app = Celery('namesgames')
# app.conf.timezone = 'UTC'
# app.config_from_object("django.conf:settings")
# app.autodiscover_tasks(settings.INSTALLED_APPS)
import os

from celery import bootsteps
from celery import Celery
from celery.schedules import crontab  # scheduler
from kombu import Exchange
from kombu import Queue

# default django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "namesgames.settings")

# variables for celery dlx and dlq
default_queue_name = "default"
default_exchange_name = "default"
default_routing_key = "default"
deadletter_sufix = "deadletter"

deadletter_queue_name = default_queue_name + f".{deadletter_sufix}"
deadletter_exchange_name = default_exchange_name + f",{deadletter_sufix}"
deadletter_routing_key = default_routing_key + f",{deadletter_sufix}"


class DeclareDLXnDLQ(bootsteps.StartStopStep):
    """
    Celery Bootstep to declate the DL exchange and queue bofore the worker starts
    processing tasks
    https://medium.com/@hengfeng/how-to-create-a-dead-letter-queue-in-celery-rabbitmq-401b17c72cd3
    """

    requires = {"celery.worker.components:Pool"}

    def start(self, worker):
        app = worker.app

        # Declare DLX and DLQ
        dlx = Exchange(deadletter_exchange_name, type="direct")

        dead_letter_queue = Queue(
            deadletter_queue_name, dlx, routing_key=deadletter_routing_key
        )

        with worker.app.pool.acquire() as conn:
            dead_letter_queue.bind(conn).declare()


app = Celery("namesgames")

app.conf.timezone = "UTC"

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

default_exchange = Exchange(default_exchange_name, type="direct")
default_queue = Queue(
    default_queue_name,
    default_exchange,
    routing_key=default_routing_key,
    queue_arguments={
        "x-dead-letter-exchange": deadletter_exchange_name,
        "x-dead-letter_routing_key": deadletter_routing_key,
    },
)

app.conf.task_queue = (default_queue,)

# Add steps to workers that declare DLX & DLQ if they don't exist
app.steps["worker"].add(DeclareDLXnDLQ)

app.conf.task_default_queue = default_queue_name
app.conf.task_default_exchange = default_exchange_name
app.conf.task_default_routing_key = default_routing_key


app.conf.beat_schedule = {
    # executes every 1 minute
    "scraping-task-one-min": {
        "task": "scraping.tasks.scraping_response",
        "schedule": crontab(),
        "options": {"routing_key": default_routing_key, "queue": default_queue_name},
    },
    # 'scraping-task-too-one-min': {
    #     'task': 'scraping.tasks.div',
    #     'schedule': crontab(),
    #     'args': (1, 0),
    #     'options': {'routing_key': default_routing_key, 'queue': default_queue_name}
    # },
    # # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute='*/15')
    # },
    # # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute=0, hour=0)
    # }
}
