from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from .validators import phone_regex


class UserManager(BaseUserManager):
    def create_user(self, email, username,  password=None, is_company_owner=False, is_staff=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),

        )
        user.staff = is_staff
        user.username = username
        user.company_owner = is_company_owner
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")

        user = self.create_user(
            email,
            username,
            is_staff=True,

            password=password,
        )
        return user

    def create_superuser(self, email, username,  password=None):
        user = self.create_user(
            email,
            username,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True

        user.is_active = True

        return user


class User(AbstractUser):
    picture_url = models.URLField(max_length=100, blank=True)
    position = models.CharField(max_length=50, blank=True)
    profile_url = models.URLField(max_length=100, blank=True)
    birthday = models.DateField(blank=True, null=True)
    company_owner = models.BooleanField(_('User could CRUD company users'), default=False)
    phone_number = models.CharField(validators=[phone_regex()], max_length=17, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    company = models.ForeignKey('Company', related_name='company_employees', on_delete=models.CASCADE, null=True)
    staff = models.BooleanField(default=False)  # a admin

    # USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['email']
    objects = UserManager()


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    @property
    def is_company_owner(self):
        return self.company_owner

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    class Meta:
        ordering = ['company']


class Company(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(_('company slug'), help_text="slug field", unique=True, max_length=100)
    last_parsed_at = models.DateTimeField(auto_now_add=True, help_text="las-modified")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_parsed_at']
