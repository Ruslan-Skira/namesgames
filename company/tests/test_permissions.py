import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts.tests.factories.user_factory import EmployeeFactory
from company.models import Company
from company.serializers import CompanySerializer
from company.tests.base import BaseTestCase

client = APIClient()


class CompanyCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = Company.objects.create(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = Company.objects.create(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.test_company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_permission(self):
        """
        Tests staff create company and check it.
        """
        data = {
            "name": "Test company 3",
        }
        client.login(email=self.staff.email, password="swordfish")
        response = client.post(reverse("companies-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test get company with unauthorized user
        client.logout()
        company = Company.objects.get(slug="test-company-3")
        serializer = CompanySerializer(company)
        self.assertGreaterEqual(serializer.data.items(), data.items())
