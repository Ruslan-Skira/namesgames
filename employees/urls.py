from rest_framework import routers

from .views import EmployeeViewSet

router = routers.DefaultRouter()

router.register(r"", EmployeeViewSet, basename="employees")
urlpatterns = router.urls
