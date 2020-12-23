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
from .permissions import IsCompanyEmployee, user_is_staff
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



class CompanyViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint that allows Company to be viewed or edited.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        if user_is_staff(self.request.user):
            company_data = request.data
            new_company = Company.objects.create(name=company_data["name"])
            new_company.save()
            serializer = CompanySerializer(new_company)
            return Response(serializer.data)
        raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        print('++++++++++++============++++++++++++++++++++++++++++++++')
        # company_name = request.query_params.get('name')
        # print(company_name, '+++++++++++++++++==================+++++++++++++++++')
        if user_is_staff(self.request.user):
            instance = self.get_object()
            self.perform_destroy(instance)
            # company = Company.objects.get(name=company_name)
            # company.delete()
            return Response({'message': f"Company has been deleted"})
        raise PermissionDenied

    @action(methods=['get'], detail=True, permission_classes=[IsCompanyEmployee],
            url_path='employees', url_name='employees')
    def get_company_employees(self, request, slug=None):
        company_employees = User.objects.filter(company__slug=slug)
        serializer = EmployeeSerializer(company_employees, many=True, context={'request': request})
        return Response(serializer.data)

    # (SerializerMapMixin,
    #  mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    #  mixins.UpdateModelMixin, mixins.ListModelMixin,
    #  mixins.DestroyModelMixin, viewsets.GenericViewSet):

    # TODO if  user do not allow return forbidden 403.
    # TODO TEst it 1. create company
    # 2.create owner
    # 3. get api by owner
    #4. return company
    # test2
    # 1. not company owner
    #2. return 403
    #test3
    #1. User not this company

    #TODO test for list company
    #1. owner one company, employee second company
    #1. users should see all the companies from api
    #2. and not authentificated user should see the all companies.

    # TODO: create, update APIs. It should be accessible only for staff (User.is_staff=True). Maybe use permission class for that
    # Important:
    #  * use serializers for input/output
    #  * make sure they're displayed in Swagger
    # like https://i.imgur.com/GxRXVZg.png

    #TODO Crete comapany test
    # 1. only staff can create company
    # 2. if it not staff during craating PUT should return 403 response.


    # TODO Test it GET api company
    #  1. create company
    #  2.create owner
    #  3. get api by owner
    #  4. return company
    # test2
    # 1. not company owner
    #2. return 403
    #test3
    #1. User not this company

# TODO: remove bellow
class CompanyEmployeesView(APIView):
    """
    API endpoint that allows Company Employees to be viewed or edited.
    """

    def get(self, request, slug):
        company_employees = User.objects.filter(company__slug=slug)
        serializer = EmployeeSerializer(company_employees, many=True, context={'request': request})
        return Response(serializer.data)
