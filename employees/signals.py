import logging
import uuid

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User
from company.tasks import company_employees_counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=User, dispatch_uid=uuid.uuid4())
def employee_create_handler(instance=None, update_fields=None, **kwargs) -> None:
    company = instance.company
    logger.info(update_fields, kwargs)
    if company:
        company_employees_counter.delay(company.id)
