import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from .filters import EmployeeByCompanyFilter
from .models import Company
from .permissions import IsCompanyEmployeeOrAdmin, IsCompanyOwnerOrAdmin, PermissionsMapMixin
from .serializers import CompanySerializer, EmployeeSerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


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
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """
    pagination_class = EmployeePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EmployeeByCompanyFilter
    permission_classes_map = {
        'create': (IsCompanyOwnerOrAdmin(),),
        'update': (IsCompanyOwnerOrAdmin(),),
        'destroy': (IsCompanyOwnerOrAdmin(),),
        'list': (permissions.IsAdminUser(),),
        'by_company': (IsCompanyEmployeeOrAdmin(),),
    }

    @action(detail=False, methods=['get'], url_path='by_company/(?P<company_slug>[^/.]+)', url_name='by_company')
    def by_company(self, request, company_slug: str):
        # https://stackoverflow.com/questions/50425262/django-rest-framework-pass-extra-parameter-to-actions
        queryset = User.objects.filter(company__slug=company_slug)  # TODO: use denormalized field

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EmployeeSerializer(data=queryset, many=True)
            serializer.is_valid()
            return self.get_paginated_response(serializer.data)
        serializer = EmployeeSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    permission_classes = [permissions.IsAdminUser]
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'

    queryset = User.objects.all()
