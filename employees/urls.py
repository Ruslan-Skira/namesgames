from rest_framework import routers

router = routers.DefaultRouter()

from .views import EmployeeViewSet

router.register(r"", EmployeeViewSet, basename="employees")
urlpatterns = router.urls
