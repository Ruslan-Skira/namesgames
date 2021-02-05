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
from .permissions import IsCompanyOwner
from .permissions import IsCompanyOwnerOrAdmin
from .permissions import PermissionsMapMixin
from .serializers import CompanySerializer
from accounts.models import User
from accounts.serializers import AdminEmployeeSerializer
from accounts.serializers import EmployeeSerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EmployeeRegisterView(RegisterView):
    queryset = User.objects.all()


class EmployeePagination(PageNumberPagination):
    """
    Pagination for additional by_company method
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


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


class EmployeeViewSet(
    PermissionsMapMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    queryset = User.employees.all()
    serializer_class = EmployeeSerializer

    pagination_class = EmployeePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EmployeeByCompanyFilter
    permission_classes = [permissions.IsAuthenticated]
    # TODO: need to be changed the permissions to IsCompanyOwner because Admin have his own endpoint.

    permission_classes_map = {
        "list": (permissions.IsAdminUser(),),
        "create": (IsCompanyOwner(),),
        "retrieve": (IsCompanyEmployeeOrAdmin(),),
        "update": (IsCompanyOwnerOrAdmin(),),
        "destroy": (IsCompanyOwner(),),
    }

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.user.company_id)

    @action(
        detail=False,
        methods=["get"],
        url_path="by_company/(?P<company_slug>[^/.]+)",
        url_name="by_company",
    )
    def by_company(self, request, company_slug: str):
        """
        Additional endpoint for getting employees by company.
        """

        company = get_object_or_404(Company, slug=company_slug)
        has_company_permission = IsCompanyEmployeeOrAdmin().has_object_permission(
            request, self, company
        )
        if not has_company_permission:
            self.permission_denied(
                request,
                message="You do not have permission to obtain all company employees.",
            )

        queryset = User.objects.filter(company_id=company.id)
        employees = self.paginate_queryset(queryset)
        serializer = EmployeeSerializer(employees, many=True)
        return self.get_paginated_response(serializer.data)


class AdminEmployeeViewSet(PermissionsMapMixin, mixins.CreateModelMixin):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    queryset = User.employees.all()
    serializer_class = AdminEmployeeSerializer

    pagination_class = EmployeePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EmployeeByCompanyFilter
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_map = {
        "list": (permissions.IsAdminUser(),),
        "create": (IsCompanyOwnerOrAdmin(),),
        "retrieve": (IsCompanyEmployeeOrAdmin(),),
        "update": (IsCompanyOwnerOrAdmin(),),
        "delete": (IsCompanyOwnerOrAdmin(),),
    }
