from celery import shared_task

from company.models import Company


@shared_task
def count_company_employees(pk) -> None:
    company = Company.objects.get(pk=pk)
    company.employees_count = int(company.employees.count())
    company.save()
