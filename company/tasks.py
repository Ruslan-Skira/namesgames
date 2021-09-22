from celery import shared_task

from company.models import Company


@shared_task
def count_company_employees(pk) -> None:
    company = Company.objects.get(pk=pk)
    company.employees_count = int(company.employees.count())
    company.save()


# def send_confirmation_email(email: str) -> None:
#     """
#     Send email if admin create company owner. For the confirmation.
#     """
#     sg.send_sendgrid_email()
#     send_mail(
#         'test message',
#         'Hello there. This is test message interesting it will came or not',
#         'hubert.nills@gmail.com',
#         ['skira.ruslan@gmail.com'],
#         fail_silently=False,)
