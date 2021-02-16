from rest_framework import routers

from .views import CompanyViewSet

router = routers.DefaultRouter()
router.register("", CompanyViewSet, basename="companies")
# router.register(r'admin/employees/', AdminEmployeeViewSet, basename='admin_employees')


urlpatterns = router.urls
