from django.core.mail import send_mail


def send(user_email):
    send_mail(
        ':You ara lucky',
        "we will write you  A lot of spam",
        "hubert.nills@gmail.com",
        [user_email],
        fail_silently=False,
    )