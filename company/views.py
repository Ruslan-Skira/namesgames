import logging

from rest_framework import mixins, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from .models import Company
from .permissions import IsCompanyOwner
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


# TODO: tests
class CompanyViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    API endpoint that allows Company to be viewed or edited.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsCompanyOwner]

    # TODO: create, update APIs. It should be accessible only for staff (User.is_staff=True). Maybe use permission class for that
    # Important:
    #  * use serializers for input/output
    #  * make sure they're displayed in Swagger
    # like https://i.imgur.com/GxRXVZg.png


# TODO: remove bellow
class CompanyEmployeesView(APIView):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    def get(self, request, slug):
        company_employees = User.objects.filter(company__slug=slug)
        serializer = EmployeeSerializer(company_employees, many=True, context={'request': request})
        return Response(serializer.data)
