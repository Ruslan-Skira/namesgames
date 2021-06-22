import arrow
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


def _regenerate_field_for_soft_deletion(obj, field_name):
    timestamp = arrow.utcnow().timestamp()
    max_length = obj.__class__._meta.get_field(field_name).max_length
    slug_suffix = f"-deleted-{str(timestamp)}"
    new_slug = getattr(obj, field_name)
    if len(new_slug) + len(slug_suffix) > max_length:
        cutoff = max_length - len(slug_suffix)
        new_slug = obj.slug[:cutoff]
    return new_slug + slug_suffix


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).is_alive
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hart_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet).delete()

    @property
    def is_alive(self):
        return self.filter(deleted_at=None)

    @property
    def is_dead(self):
        return self.exclude(deleted_at=None)
