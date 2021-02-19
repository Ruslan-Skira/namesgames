from celery import shared_task

from company.models import Company


@shared_task
def company_employees_counter(pk) -> None:
    company = Company.objects.get(pk=pk)
    company.employees_count = int(
        company.company_employees.exclude(deleted_at__isnull=False).count()
    )
    company.save()
