from .base import *  # NOQA


DEBUG = True
LOGGING_CONFIG = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "file_format",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            # create file before
            "filename": "/home/user/Projects/linkedingame/namesgames/namesgames/debug.log",
            "formatter": "file_format",
        },
    },
    "loggers": {
        # root logger
        "": {
            "handlers": ["console"],
            "propagate": True,
            # 'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        "user.views": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "django.utils.autoreload": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    },
    "formatters": {
        "file_format": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
}

# logging.config.dictConfig(LOGGING)
# TOKEN_FILE = 'scraping/token.pickle'
# NAMESGAMES_ADDRESS = 'namesgames.com'

# read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
# 'default': env.db(),




ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost"]
