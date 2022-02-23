from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from company.models import Company
from accounts.models import User
from faker import Faker

from company.tasks import send_welcome_email

fake = Faker()


@receiver(post_save, sender=Company, )
def create_user_owner(instance=None, created=True, update_fields=None, **kwargs):
    # User.objects.username = fake.name()
    # User.objects.is_company_owner = True
    # User.objects.email = fake.email()
    # User.objects.company = Company.pk

    user = User.objects.create_user(email=fake.email(), password="password", is_company_owner=True, company=instance)
    send_welcome_email.delay(
        email=user.email
    )


# @receiver(post_save, sender=Company, )
# def send_mail(instance=None, created=True, update_fields=None, **kwargs):
#     # send_welcome_email.delay(
#     #     email=User.objects.get(instance.email)
#     # )
