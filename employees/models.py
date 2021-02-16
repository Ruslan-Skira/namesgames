from django.db import models
from django.db.models import Q


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(Q(is_superuser=True) | Q(company=None))
