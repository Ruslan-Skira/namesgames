import logging

from dj_rest_auth.registration.views import RegisterView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from .filters import EmployeeByCompanyFilter
from .models import Company
from .permissions import IsCompanyEmployeeOrAdmin
from .permissions import IsCompanyOwnerOrAdmin
from .permissions import PermissionsMapMixin
from .serializers import CompanySerializer
from .serializers import EmployeeSerializer
from accounts.models import User

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EmployeeRegisterView(RegisterView):
    queryset = User.objects.all()


class CompanyViewSet(PermissionsMapMixin,
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


class EmployeePagination(PageNumberPagination):
    """
    Pagination for additional by_company method
    """
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeViewSet(PermissionsMapMixin, mixins.ListModelMixin, GenericViewSet):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'

    pagination_class = EmployeePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EmployeeByCompanyFilter

    # permission_classes = [permissions.IsAdminUser]
    permission_classes_map = {
        'list': (permissions.IsAdminUser(),),
    }

    @action(detail=False, methods=['get'], url_path='by_company/(?P<company_slug>[^/.]+)', url_name='by_company')
    def by_company(self, request, company_slug: str):
        company = get_object_or_404(Company, slug=company_slug)
        has_company_permission = IsCompanyEmployeeOrAdmin().has_object_permission(request, self, company)
        if not has_company_permission:
            self.permission_denied(
                request, message='You do not have permission to get all the users by company')

        queryset = User.objects.filter(company_id=company.id)
        employees = self.paginate_queryset(queryset)
        serializer = EmployeeSerializer(employees, many=True)
        return self.get_paginated_response(serializer.data)
