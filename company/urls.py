from django.urls import path

from .views import CompanyEmployeesView, CompanyViewSet

urlpatterns = [
    # TODO: use DRF router and only use CompanyViewSet. delete

    path("companies/", CompanyViewSet.as_view(), name='companies'),
    # path("company/<slug:slug>/", CompanyView.as_view({'get': 'list'}), name='company'),
    # path("employees", EmployeeViewSet.as_view(), name='company_employees'),

]
