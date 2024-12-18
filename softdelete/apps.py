from django.apps import AppConfig


class SoftdeleteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "softdelete"

    def ready(self):
        from softdelete import receivers  # noqa
