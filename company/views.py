import logging

from rest_framework import mixins, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied


from accounts.models import User
from .models import Company
from .permissions import PermissionsMapMixin, IsCompanyOwnerOrAdmin
from .serializers import CompanySerializer, EmployeeSerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(
                    PermissionsMapMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    API endpoint that allows Company to be viewed or edited.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'slug'

    permission_classes_map = {
        'create': (permissions.IsAdminUser(),),
        'update': (IsCompanyOwnerOrAdmin(),)
    }


class CompanyEmployeesView(APIView):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    def get(self, request, slug):
        company_employees = User.objects.filter(company__slug=slug)
        serializer = EmployeeSerializer(company_employees, many=True, context={'request': request})
        return Response(serializer.data)
