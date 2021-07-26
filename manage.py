#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
import logging.config
#
# LOGGING_CONFIG = None
# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             # exact format is not important, this is the minimum information
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#         },
#     },
#     'loggers': {
#         # root logger
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#     },
# })


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'namesgames.settings.staging')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
