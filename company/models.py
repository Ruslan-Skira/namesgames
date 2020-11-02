from django.db import models
from django.template.defaultfilters import slugify

from .validators import phone_regex


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture_url = models.URLField(max_length=100)
    position = models.CharField(max_length=50)
    profile_url = models.URLField(max_length=100)
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=50)

    phone_number = models.CharField(validators=[phone_regex()], max_length=17, blank=True)
    skype = models.CharField(max_length=50)
    company = models.ForeignKey('Company', related_name='company_employees', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['company']


class Company(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(help_text="slug field", unique=True, max_length=100)
    last_parsed_at = models.DateTimeField(auto_now_add=True, help_text="las-modified")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_parsed_at']
