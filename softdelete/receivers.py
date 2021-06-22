import logging

from django.dispatch import receiver

from company.tasks import count_company_employees
from softdelete import signals

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@receiver(signals.soft_delete_signal)
def employee_soft_delete_handler(sender, **kwargs):
    """
    Handler for soft delete model.
    """
    company = sender.company
    if company:
        logger.info(
            f" {sender.email} is updated. "
            f"Scheduling the task to recalculate employee_count",
            kwargs,
        )
        count_company_employees.delay(company.id)
