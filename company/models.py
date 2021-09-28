from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from softdelete.models import _regenerate_field_for_soft_deletion, SoftDeletionModel


class Company(SoftDeletionModel):
    """
    Company model
    """

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        _("company slug"), help_text="slug field", unique=True, max_length=100
    )
    last_parsed_at = models.DateTimeField(auto_now_add=True, help_text="las-modified")
    employees_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    def delete(self, using=None, keep_parents=False):
        """
        Rewrite delete method to soft delete method.
        """

        # Rename company to prevent collisions
        self.name = _regenerate_field_for_soft_deletion(self, "name")
        # SoftDeleteModel.delete() saves the object, so no need to save it here.
        return super().delete()

    def save(self, *args: list, **kwargs: dict) -> None:
        """
        During the save slug will be created from company name.
        """

        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def all_employees(self) -> None:
        """
        Method return all employees.
        """
        return User.all_objects.filter(company=self.id)

    class Meta:
        ordering = ["last_parsed_at"]
        verbose_name_plural = "Companies"
