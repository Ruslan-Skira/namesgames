from .dev import *  # NOQA

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "namesgames",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": 5432,
    }
}