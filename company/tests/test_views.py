import datetime
from unittest import skip

import pytest
from django.contrib.contenttypes.models import ContentType
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts.tests.factories.user_factory import EmployeeFactory
from company.models import Company
from company.serializers import CompanySerializer
from company.tests.base import BaseTestCase
from company.views import EmployeeViewSet

client = APIClient()


@tag('company')
@pytest.mark.django_db(transaction=True)
# class CompanyTest(BaseTestCase):
#     """Test module for GET all companies API"""
#
#     def setUp(self):
#         ContentType.objects.clear_cache()
#         super(CompanyTest, self).setUp()
#         self.test_company = Company.objects.create(
#             name='TestCompanyAPI-1', last_parsed_at=datetime.datetime.today())
#         self.test_company2 = Company.objects.create(
#             name='TestCompanyAPI-2', last_parsed_at=datetime.datetime.today())
#
#         self.staff = EmployeeFactory(is_staff=True, is_active=True)
#         self.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company=self.test_company)
#         self.employee_test_company = EmployeeFactory(is_active=True, company=self.test_company)
#         # self.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company_id=self.test_company.id)
#
#     def test_get_all_companies(self):
#         response = client.get(reverse('companies-list'))
#         companies = Company.objects.all()
#         serializer = CompanySerializer(companies, many=True)
#         self.assertEqual(response.data['results'], serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_one_company(self):
#         response = client.get(
#             reverse('companies-detail', kwargs={'slug': self.test_company.slug}))
#         data = {
#             "name": self.test_company.name,
#             "slug": self.test_company.slug,
#         }
#         self.assertGreaterEqual(response.data.items(), data.items())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_one_company_invalid_slug(self):
#         response = client.get(
#             reverse('companies-detail', kwargs={'slug': self.test_company.slug + 'invalidslug'}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_create_company_is_staff(self):
#         """
#         Tests staff create company and check it.
#         """
#         data = {
#             "name": "Test company 3",
#             "slug": "test-company-3",
#         }
#         client.login(email=self.staff.email, password='swordfish')
#         response = client.post(reverse('companies-list'), data=data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # test get company with unauthorized user
#         client.logout()
#         company = Company.objects.get(slug='test-company-3')
#         serializer = CompanySerializer(company)
#         self.assertGreaterEqual(serializer.data.items(), data.items())
#
#     # @pytest.mark.django_db(transaction=True)
#     def test_create_company_is_not_staff(self):
#         """
#         Tests not staff create company and check it.
#         """
#         data = {
#             "name": "Test company 4",
#             "slug": "test-company-4",
#         }
#         response = client.post(reverse('companies-list'), data=data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_invalid_company(self):
#         response = client.get(
#             reverse('companies-detail', kwargs={'slug': 'guffy_fail_slug'}
#                     ))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_update_company(self):
#         client.force_login(self.company_owner)
#         data = {
#             "name": "updated company",
#             "slug": "updated-company"
#         }
#         response = client.put(
#             reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
#             data=data)
#
#         self.assertGreaterEqual(response.data.items(), data.items())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_update_company_not_authorized_user(self):
#         data = {
#             "name": "updated company",
#             "slug": "updated-company"
#         }
#         response = client.put(
#             reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
#             data=data)
#
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_update_company_company_employee(self):
#         client.force_login(self.employee_test_company)
#
#         data = {
#             "name": "updated company",
#             "slug": "updated-company"
#         }
#         response = client.put(
#             reverse('companies-detail', kwargs={'slug': self.test_company.slug}),
#             data=data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@tag('employee')
class EmployeeTest(BaseTestCase):
    """Test module for GET all companies API"""

    @classmethod
    def setUpClass(cls):
        cls.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        cls.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())
        cls.company_owner = EmployeeFactory(is_company_owner=True, is_active=True, company=cls.test_company)
        cls.employee_test_company = EmployeeFactory(is_active=True, company=cls.test_company)
        cls.employee_test_company2 = EmployeeFactory(is_active=True, company=cls.test_company2)

    @classmethod
    def tearDownClass(cls): ...

    def test_get_employees_by_company_valid(self):
        client.force_login(self.employee_test_company2)

        data = [{'last_name': self.employee_test_company2.last_name,
                 'picture_url': self.employee_test_company2.picture_url,
                 'position': self.employee_test_company2.position,
                 'birthday': str(self.employee_test_company2.birthday),
                 'email': self.employee_test_company2.email,
                 'phone_number': self.employee_test_company2.phone_number,
                 'skype': self.employee_test_company2.skype,
                 'company': self.test_company2.id}]

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

    def test_employee_company_slug_admin(self):
        client.force_login(self.staff)
        data = [{'last_name': self.employee_test_company.last_name,
                 'picture_url': self.employee_test_company.picture_url,
                 'position': self.employee_test_company.position,
                 'birthday': str(self.employee_test_company.birthday),
                 'email': self.employee_test_company.email,
                 'phone_number': self.employee_test_company.phone_number,
                 'skype': self.employee_test_company.skype,
                 'company': self.test_company.id},
                ]

        response = client.get(f'/api/v1/employees/?company={self.test_company}/')
        self.assertEqual(response.json()['results'], data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# def test_pagination(self):
#     EmployeeViewSet.page_size = 1
#     client.force_login(self.employee_test_company)
#     response = client.get(f'/api/v1/employees/?company={self.test_company}/')
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     self.assertEqual(len(response.json()['results']), 1)
