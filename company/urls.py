from django.urls import path

from .views import CompanyEmployeesView, CompanyView, CompanyViewSet

urlpatterns = [
    path("companies/", CompanyViewSet.as_view(), name='companies'),
    path("company/<slug:slug>/", CompanyView.as_view(), name='company'),
    path("company/<slug:slug>/employees", CompanyEmployeesView.as_view(), name='company_employees'),
]
