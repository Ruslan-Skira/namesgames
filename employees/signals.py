import logging
import uuid

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User
from company.tasks import count_company_employees

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, dispatch_uid=uuid.uuid4())
def employee_create_handler(
    instance=None, created=True, update_fields=None, **kwargs
) -> None:
    """
    User post save  signal.
    """
    company = instance.company
    if company and created:
        logger.info(
            "New employee is created. Scheduling the task to recalculate employee_count",
            update_fields,
            kwargs,
        )
        count_company_employees.delay(company.id)


@receiver(post_delete, sender=User, dispatch_uid=uuid.uuid4())
def employee_delete_handler(instance=None, update_fields=None, **kwargs) -> None:
    """
    User post delete signal.
    """
    company = instance.company
    if company:
        logger.info(
            "Employee is deleted. Scheduling the task to recalculate employee_count",
            update_fields,
            kwargs,
        )
        count_company_employees.delay(company.id)
