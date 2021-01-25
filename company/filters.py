from django_filters import rest_framework as filters

from accounts.models import User


class EmployeeByCompanyFilter(filters.FilterSet):
    """
    Filter class to find Employees by position and first_name.
    """

    class Meta:
        model = User
        fields = ["position", "first_name", "last_name"]
