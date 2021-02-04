from rest_framework import routers

from .views import CompanyViewSet
from .views import EmployeeViewSet

router = routers.DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"employees", EmployeeViewSet, basename="employees")
# router.register(r'admin/employees', AdminEmployeeViewSet, basename='admin_employees')


urlpatterns = router.urls
