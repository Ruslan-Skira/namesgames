from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail

from company.models import Company


@shared_task
def count_company_employees(pk) -> None:
    company = Company.objects.get(pk=pk)
    company.employees_count = int(company.employees.count())
    company.save()


@shared_task
def send_welcome_email(email):
    send_mail(
        'Welcome NamesGames',
        "Welcome dear owner, you must change password follow the link www.google.com",
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: '
        'nina.agneshka@gmail.com',
        [{email}],
        fail_silently=False,
    )
