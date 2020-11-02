import logging

from django.http import Http404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(APIView):
    """
    API endpoint that allows Companies to be viewed or edited.
    """

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyView(APIView):
    """
    API endpoint that allows Company to be viewed or edited.
    """

    def get(self, request, slug):
        logger.info(f'company_visited_from_get {request.session.get("company_visited")}')

        try:
            company = Company.objects.get(slug=slug)
            serializer = CompanySerializer(company)
            save_company_id(request, company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            raise Http404


def save_company_id(request, company):
    """
    Company id will saved into the user session
    """
    company_id = company.id
    company_visited = request.session.get('company_visited', None)
    if company_visited and company_id not in company_visited:
        companies_visited = request.session['company_visited']
        companies_visited.append(company_id)
        request.session['company_visited'] = companies_visited
    else:
        request.session['company_visited'] = [company_id]


class CompanyEmployeesView(APIView):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    def get(self, request, slug):
        company_employees = Employee.objects.filter(company__slug=slug)
        serializer = EmployeeSerializer(company_employees, many=True, context={'request': request})
        return Response(serializer.data)
