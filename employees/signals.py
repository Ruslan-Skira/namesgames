"""
Signals.py file
"""
import logging
import uuid
from typing import Dict, List, Optional

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User
from company.tasks import count_company_employees

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, dispatch_uid=uuid.uuid4())
def employee_create_handler(
    instance: Optional[User] = None,
    created: bool = True,
    update_fields: Optional[List] = None,
    **kwargs: Dict,
) -> None:
    """
    User post save  signal.py
    """
    if instance and created and update_fields:
        company = instance.company
        logger.info(
            f"New employee {instance.email} is created. "
            f"Scheduling the task to recalculate employee_count",
        )
        count_company_employees.delay(company.id)


@receiver(post_delete, sender=User, dispatch_uid=uuid.uuid4())
def employee_delete_handler(
    instance: Optional[User] = None,
    update_fields: Optional[List] = None,
    **kwargs: Dict,
) -> None:
    """
    User post delete signal.
    """
    if instance and update_fields:
        company = instance.company
        logger.info(
            f"Employee {instance.email} is deleted. Scheduling the task to recalculate employee_count",
            update_fields,
        )
        count_company_employees.delay(company.id)
