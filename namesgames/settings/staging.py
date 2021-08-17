from namesgames.settings.base import *  # NOQA

DEBUG = True

CELERY_BROKER_URL = "rabbitmq3"

ALLOWED_HOSTS: list = ['*']
