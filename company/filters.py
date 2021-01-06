from django.forms import SelectMultiple
from django_filters import rest_framework as filters

from accounts.models import User
from company.models import Company


class EmployeeByCompanyFilter(filters.FilterSet):
    company__slug = filters.ModelMultipleChoiceFilter(
        field_name='company__slug',
        to_field_name='slug',
        widget=SelectMultiple(),
        queryset=Company.objects.all(),
        label='slug',
    )

    class Meta:
        model = User
        fields = ['company__slug']
