import datetime

from django.test import tag, TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from company.models import Company
from company.serializers import CompanySerializer
from company.tests.factories.UserFactory import UserFactory

client = APIClient()


class GetCompanyTest(TestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())

        self.staff = UserFactory(is_staff=True, is_active=True)
        self.company_owner = UserFactory(is_company_owner=True, is_active=True, company_id=1)
        self.employee_test_company = UserFactory(is_active=True, company=self.test_company)
        # self.company_owner = UserFactory(is_company_owner=True, is_active=True, company_id=self.test_company.id)

    def test_get_all_companies(self):
        response = client.get(reverse('companies-list'))
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: test 404
    def test_get_one_company(self):
        response = client.get(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}))
        data = {
            "name": self.test_company.name,
            "slug": self.test_company.slug,
        }
        self.assertGreaterEqual(response.data.items(), data.items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO test unauthorized
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

    def test_create_company_is_not_staff(self):
        """
        Tests staff create company and check it.
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

    def test_update_company_company_employee(self):
        client.force_login(self.employee_test_company)

        data = {
            "name": "updated company",
            "slug": "updated-company"
        }
        response = client.put(
            reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@tag('employee')
class EmployeeTest(TestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())

        self.staff = UserFactory(is_staff=True, is_active=True)
        self.company_owner = UserFactory(is_company_owner=True, is_active=True, company_id=1)
        self.employee_test_company = UserFactory(is_active=True, company=self.test_company)
        # self.company_owner = UserFactory(is_company_owner=True, is_active=True, company_id=self.test_company.id)

    # TODO write the test1 employee/by_company/<copany_slug>

    def test_get_employees_by_company_slug(self):
        # from namesgames.urls import router
        # view = EmployeeViewSet()
        # view.basename = router.get_default_basename(EmployeeViewSet)
        # view.request = None
        # assert view.reverse_action('by_company') == 'blablas'

        client.force_login(self.staff)

        data = [[('last_name', ''),
                 ('picture_url', ''),
                 ('position', ''),
                 ('birthday', None),
                 ('email', 'Agent 001'),
                 ('phone_number', ''),
                 ('skype', ''),
                 ('company', 1)],
                [('last_name', ''),
                 ('picture_url', ''),
                 ('position', ''),
                 ('birthday', None),
                 ('email', 'Agent 002'),
                 ('phone_number', ''),
                 ('skype', ''),
                 ('company', 1)]]

        response = client.get('/api/v1/employees/by_company/testcompanyapi/')
        print(response.data['results'])
        # self.assertGreaterEqual(response.data.items(), data.items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: test2 list employee/<company_slug> Pemissions
    #  1. unauthorized user
    #  2. user Admin

    # TODO: test3 create': (IsCompanyOwnerOrAdmin(),),
    # TODO: TEST4'update': (IsCompanyOwnerOrAdmin(),),
    # TODO: TEST5 'destroy': (IsCompanyOwnerOrAdmin(),),
