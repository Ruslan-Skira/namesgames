import datetime

from company.models import Company
from company.serializers import CompanySerializer
from company.tests.factories.UserFactory import UserFactory
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

client = APIClient()


class GetCompanyTest(TestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        self.test_company = Company.objects.create(
            name='TestCompanyAPI', last_parsed_at=datetime.datetime.today())
        self.test_company2 = Company.objects.create(
            name='TestCompanyAPI2', last_parsed_at=datetime.datetime.today())

        self.staff = UserFactory(is_staff=True, is_active=True)

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
