from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


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
