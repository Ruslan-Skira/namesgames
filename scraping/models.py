from django.db import models
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify


class People(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2083, default="", unique=True)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    source = models.CharField(max_length=30, default="", blank=True, null=True)


class Employee(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    picture_url = models.URLField(max_length=200)
    position = models.CharField(max_length=200)
    profile_url = models.URLField(max_length=200)
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    skype = models.CharField(max_length=50)
    company = models.ForeignKey('Company', related_name='company_employees', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name}\n {self.last_name}'


class Company(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(help_text="slug field", unique=True, max_length=100)
    last_parced_at = models.DateTimeField(auto_now_add=True, help_text="las-modified")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
