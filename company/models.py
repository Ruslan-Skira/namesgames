from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
import arrow

from namesgames.models import SoftDeletionModel


def _regenerate_field_for_soft_deletion(obj, field_name):
    timestamp = arrow.utcnow().timestamp
    print(dir(obj.__class__), '---------=========================------------')
    max_length = obj.__class__._meta.get_field(field_name).max_length
    slug_suffix = '-deleted-{}'.format(str(timestamp))
    new_slug = getattr(obj, field_name)
    if len(new_slug) + len(slug_suffix) > max_length:
        cutoff = max_length - len(slug_suffix)
        new_slug = obj.slug[:cutoff]
    return new_slug + slug_suffix


class Company(SoftDeletionModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(_('company slug'), help_text="slug field", unique=True, max_length=100)
    last_parsed_at = models.DateTimeField(auto_now_add=True, help_text="las-modified")

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        # Rename company to prevent collisions
        self.name = _regenerate_field_for_soft_deletion(self, 'name')
        # SoftDeleteModel.delete() saves the object, so no need to save it here.
        return super(Company, self).delete()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_parsed_at']
