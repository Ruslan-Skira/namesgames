import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: use pre_save signal

@receiver(pre_save, sender=User)
def employee_create_handler( sender, instance=None, created=None, update_fields=None, **kwargs):
    company = instance.company
    logger.info(update_fields, kwargs)
    if company:
        company.employees_count = int(company.company_employees.exclude(deleted_at__isnull=False).count())
        company.save()
