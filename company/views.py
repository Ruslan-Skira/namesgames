import logging

from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from .models import Company
from .permissions import IsCompanyOwnerOrAdmin, PermissionsMapMixin, IsCompanyEmployeeOrAdmin
from .serializers import CompanySerializer, EmployeeSerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# class EmployeeViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for viewing and editing the accounts
#     associated with the user.
#     """
#     queryset = User.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(
    PermissionsMapMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    """
    API endpoint that allows Company to be viewed or edited.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'slug'

    permission_classes_map = {
        'create': (permissions.IsAdminUser(),),
        'update': (IsCompanyOwnerOrAdmin(),),
        'destroy': (permissions.IsAdminUser(),),
    }


class EmployeeViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """
    permission_classes_map = {
        'create': (IsCompanyOwnerOrAdmin(),),
        'update': (IsCompanyOwnerOrAdmin(),),
        'destroy': (IsCompanyOwnerOrAdmin(),),
        'list': (permissions.IsAdminUser(),),
        'by_company': (IsCompanyEmployeeOrAdmin(),),
    }

    @action(detail=False, methods=['get'], url_path='by_company/(?P<company_slug>[^/.]+)')
    def by_company(self, request, company_slug, pk=None):
        # https://stackoverflow.com/questions/50425262/django-rest-framework-pass-extra-parameter-to-actions
        employees = User.objects.filter(company__slug=company_slug)
        serializer = EmployeeSerializer(data=employees, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    permission_classes = [permissions.IsAdminUser]
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'

    queryset = User.objects.all()


class CompanyEmployeesView(): ...
