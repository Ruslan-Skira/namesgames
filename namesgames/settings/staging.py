from namesgames.settings.base import *  # NOQA

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "namesgames",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}

CELERY_BROKER_URL = "rabbitmq3"
