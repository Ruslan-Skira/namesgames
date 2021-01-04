from rest_framework import routers

from .views import CompanyViewSet, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = router.urls
