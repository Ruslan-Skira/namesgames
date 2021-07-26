from namesgames.settings.base import *  # NOQA
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