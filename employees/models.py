from django.db.models import Q

from softdelete.models import SoftDeletionManager


class EmployeeManager(SoftDeletionManager):
    def get_queryset(self):
        return super().get_queryset().exclude(Q(is_superuser=True) | Q(company=None))
