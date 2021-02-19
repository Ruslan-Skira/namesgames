import logging

from rest_framework import mixins
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet

from .models import Company
from .permissions import IsCompanyOwnerOrAdmin
from .permissions import PermissionsMapMixin
from .serializers import CompanySerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class CompanyViewSet(
    PermissionsMapMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows Company to be viewed or edited.
    """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = "slug"
    permission_classes = []

    permission_classes_map = {
        "create": (permissions.IsAdminUser(),),
        "update": (IsCompanyOwnerOrAdmin(),),
        "destroy": (permissions.IsAdminUser(),),
    }
