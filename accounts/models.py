from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from .validators import phone_regex


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email,  password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password, **extra_fields):
        """
        Create and save a SuperUser with given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_company_owner', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        if extra_fields.get('is_company_owner') is not True:
            raise ValueError(_('Superuser must have is_company_owner=True.'))

        return self.create_user(email, password, **extra_fields)


# TODO after put it on production could occurs error read it
#  https://stackoverflow.com/questions/14386536/instantiating-django-model-raises-typeerror-isinstance-arg-2-must-be-a-class
class User(AbstractUser):
    username = None
    picture_url = models.URLField(max_length=100, blank=True)
    position = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(blank=True, null=True)
    is_company_owner = models.BooleanField(_('User could CRUD company users'), default=False)
    phone_number = models.CharField(validators=[phone_regex()], max_length=17, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_('Email address'), unique=True, blank=True)
    company = models.ForeignKey('company.Company', related_name='company_employees', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['company']
