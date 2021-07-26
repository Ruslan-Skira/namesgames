from namesgames.settings.base import *  # NOQA

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "namesgames",
        "USER": "namesgames_admin",
        "PASSWORD": "1q2w3e4r5t6y",
        "HOST": "namesgames.c0a07epeefme.us-east-2.rds.amazonaws.com",
        "PORT": 5432,
    }
}

CELERY_BROKER_URL = "rabbitmq3"

ALLOWED_HOSTS=['*']