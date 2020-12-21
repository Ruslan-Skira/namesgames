from django.urls import path

from .views import CompanyEmployeesView, CompanyViewSet

urlpatterns = [
    path("companies/", CompanyViewSet.as_view(), name='companies'),
]
