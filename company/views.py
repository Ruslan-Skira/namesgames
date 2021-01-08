import logging

from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status
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
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeViewSet(mixins.ListModelMixin, GenericViewSet):
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
        # 'by_company': (IsCompanyEmployeeOrAdmin(),),
    }

    @action(detail=False, methods=['get'], url_path='by_company/(?P<company_slug>[^/.]+)', url_name='by_company')
    def by_company(self, request, company_slug: str):

        # TODO: check that current user has permissions to view employees of given company. if not, raise exception (Forbbidden, NotAllowed etc.)
        #       1. do it yourself
        #       2. use IsCompanyEmployeeOrAdmin()
        if request.user.company.slug == company_slug:
            queryset = get_list_or_404(User, company__slug=company_slug)# TODO: use denormalized field

            employees = self.paginate_queryset(queryset)
            serializer = EmployeeSerializer(employees, many=True)
            return self.get_paginated_response(serializer.data)
        else: Response(status=status.HTTP_403_FORBIDDEN)

