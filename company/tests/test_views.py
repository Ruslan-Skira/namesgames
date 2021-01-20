import datetime

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import settings
from rest_framework.test import APIClient

from accounts.tests.factories.user_factory import EmployeeFactory
from company.models import Company
from company.serializers import CompanySerializer
from company.tests.base import BaseTestCase

client = APIClient()


class CompanyTest(BaseTestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        ContentType.objects.clear_cache()
        super(CompanyTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI-1', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI-2', last_parsed_at=datetime.datetime.today())

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company=self.test_company)
        self.employee_test_company = EmployeeFactory(is_active=True, company=self.test_company)
        # self.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company_id=self.test_company.id)

    def test_get_all_companies(self):
        response = client.get(reverse('companies-list'))
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_company(self):
        response = client.get(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}))
        data = {
            "name": self.test_company.name,
            "slug": self.test_company.slug,
        }
        self.assertGreaterEqual(response.data.items(), data.items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_company_invalid_slug(self):
        response = client.get(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug + 'invalidslug'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_company_is_staff(self):
        """
        Tests staff create company and check it.
        """
        data = {
            "name": "Test company 3",
            "slug": "test-company-3",
        }
        client.login(email=self.staff.email, password='swordfish')
        response = client.post(reverse('companies-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test get company with unauthorized user
        client.logout()
        company = Company.objects.get(slug='test-company-3')
        serializer = CompanySerializer(company)
        self.assertGreaterEqual(serializer.data.items(), data.items())

    # @pytest.mark.django_db(transaction=True)
    def test_create_company_is_not_staff(self):
        """
        Tests not staff create company and check it.
        """
        data = {
            "name": "Test company 4",
            "slug": "test-company-4",
        }
        response = client.post(reverse('companies-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_company(self):
        response = client.get(
            reverse('companies-detail', kwargs={'slug': 'guffy_fail_slug'}
                    ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_company(self):
        client.force_login(self.company_owner)
        data = {
            "name": "updated company",
            "slug": "updated-company"
        }
        response = client.put(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
            data=data)

        self.assertGreaterEqual(response.data.items(), data.items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_not_authorized_user(self):
        data = {
            "name": "updated company",
            "slug": "updated-company"
        }
        response = client.put(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
            data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_employee(self):
        client.force_login(self.employee_test_company)

        data = {
            "name": "updated company",
            "slug": "updated-company"
        }
        response = client.put(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EmployeeTest(BaseTestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        super(EmployeeTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())
        self.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company=self.test_company)
        self.employee_test_company = EmployeeFactory(is_active=True, company=self.test_company)
        self.employee_test_company2 = EmployeeFactory(is_active=True, company=self.test_company2)

    def test_get_employees_by_company_valid(self):
        client.force_login(self.employee_test_company2)

        data = [{'last_name': self.employee_test_company2.last_name,
                 'picture_url': self.employee_test_company2.picture_url,
                 'position': self.employee_test_company2.position,
                 'birthday': str(self.employee_test_company2.birthday),
                 'email': self.employee_test_company2.email,
                 'phone_number': self.employee_test_company2.phone_number,
                 'skype': self.employee_test_company2.skype,
                 'company': self.test_company2.id,
                 'id': self.employee_test_company2.id}]

        response = client.get(f'/api/v1/employees/by_company/{self.test_company2.slug}/', format='json')
        self.assertEqual(response.json()['results'], data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_by_company_not_valid_company_slug(self):
        client.force_login(self.staff)
        response = client.get('/api/v1/employees/by_company/not-valid-testcompanyapi/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_by_company_not_authorized_user(self):
        response = client.get(f'/api/v1/employees/by_company/{self.test_company.slug}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # employees endpoint

    def test_employee_company_slug_not_valid(self):
        response = client.get('/api/v1/employees/not-valid-testcompanyapi/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_company_slug_unauthorized(self):
        response = client.get(f'/api/v1/employees/?company={self.test_company2}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_company_slug_not_employee(self):
        client.force_login(self.employee_test_company)

        response = client.get(f'/api/v1/employees/?company={self.test_company2}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_employees_filter_company(self):
        client.force_login(self.staff)

        response = client.get(f'/api/v1/employees/?company={self.test_company}/')
        self.assertEqual(len(response.json()['results']), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EmployeePaginationPageTest(BaseTestCase):
    def setUp(self):
        super(EmployeePaginationPageTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        [EmployeeFactory(is_active=True, company=self.test_company) for _ in range(20)]

    def test_pagination(self):
        client.force_login(self.staff)
        response = client.get(f'/api/v1/employees/?company={self.test_company}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), settings.REST_FRAMEWORK['PAGE_SIZE'])


class EmployeesGetTest(BaseTestCase):
    def setUp(self):
        super(EmployeesGetTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI-1', last_parsed_at=datetime.datetime.today())
        self.employee_test_company1 = EmployeeFactory(is_active=True, company=self.test_company)
        self.employee_test_company2 = EmployeeFactory(is_active=True, company=self.test_company)
        self.employee_test_company3 = EmployeeFactory(is_active=True, company=self.test_company)
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "password1": "swordfish",
            "password2": "swordfish",
        }

    def test_get_all_employees(self):
        """
        Test should check the GET response length of the list with users
        admin + companyowner + 2test_employee = 4 users
        """
        client.force_login(self.staff)
        response = client.get(f'/api/v1/employees/')
        self.assertEqual(len(response.json()['results']), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user(self):
        client.force_login(self.staff)
        """
        Test GET one employee.
        """

        response = client.get(f'/api/v1/employees/{self.employee_test_company1.id}/')
        self.assertEqual(response.data['email'], self.employee_test_company1.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_employees_not_valid(self):
        """
        Test GET should check negative test case.
        """
        response = client.get('/api/v1/employees/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeCreateTest(BaseTestCase):
    def setUp(self):
        super(EmployeeCreateTest, self).setUp()
        self.tes_user_data = {
            "email": "test_user_3@user.com",
            "password1": "swordfish",
            "password2": "swordfish",
        }

    def test_create_new_users(self):
        client.force_login(self.staff)
        """
        Test POST should check how admin could create Employees.
        """
        response = client.post('/api/v1/employees/', data=self.tes_user_data)
        self.assertGreaterEqual(list(response.data.items()), list(self.tes_user_data.items()))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_users_not_valid(self):
        """
        Test POST with not valid user.
        """
        response = client.post('/api/v1/employees/', data=self.tes_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeUpdateTest(BaseTestCase):
    def setUp(self):
        super(EmployeeUpdateTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI-1', last_parsed_at=datetime.datetime.today())
        self.employee_test_company = EmployeeFactory(is_active=True, company=self.test_company)
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "skype": 'test3Skype',
            "position": "employee1",
        }

    def test_update_user(self):
        client.force_login(self.staff)
        """
        Test UPDATE should check how admin could update Employee.
        """

        response = client.put(f'/api/v1/employees/{self.employee_test_company.id}/', data=self.test_user_data)
        self.assertGreaterEqual(list(response.data.items()), list(self.test_user_data.items()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_not_valid(self):
        """
        Test UPDATE should return 403 because user not allowed to do update.
        """

        response = client.put(f'/api/v1/employees/{self.employee_test_company.id}/', data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeDeleteTest(BaseTestCase):
    def setUp(self):
        super(EmployeeDeleteTest, self).setUp()
        self.test_company = Company.objects.create(
            name='TestCompanyAPI-1', last_parsed_at=datetime.datetime.today())
        self.employee_test_company = EmployeeFactory(is_active=True, company=self.test_company)

    def test_delete_user(self):
        client.force_login(self.staff)
        """
        Test DELETE should check how admin could delete Employee.
        """
        response = client.delete(f'/api/v1/employees/{self.employee_test_company.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_not_valid(self):
        """
        Test DELETE should check how admin could delete Employee.
        """
        response = client.delete(f'/api/v1/employees/{self.employee_test_company.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
