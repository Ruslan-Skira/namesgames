import datetime
from unittest.mock import MagicMock

from rest_framework.test import APIClient

from accounts.tests.factories.user_factory import EmployeeFactory
from company.permissions import IsCompanyEmployeeOrAdmin, IsEmployee, IsCompanyOwner
from company.tests.base import BaseTestCase
from company.tests.factories.company_factory import CompanyFactory

clipent = APIClient()


class PermissionTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.user = MagicMock()
        self.user.is_superuser = True
        self.request_by_admin = MagicMock(user=self.staff)
        self.view = MagicMock()

        self.company = CompanyFactory(
            name="TestCompanyAPI", last_parsed_at=datetime.datetime.today()
        )
        self.company2 = CompanyFactory(
            name="TestCompanyAPI2", last_parsed_at=datetime.datetime.today()
        )
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.company
        )
        self.employee_company = EmployeeFactory(
            is_active=True, company=self.company, is_superuser=True
        )
        self.request_by_employee = MagicMock(user=self.employee_company)
        self.employee_company2 = EmployeeFactory(
            is_active=True, company=self.company2
        )


class TestIsEmployee(PermissionTest):
    def setUp(self):
        super().setUp()
        self.permission = IsEmployee()

        self.employee_no_company = EmployeeFactory(
            is_active=True
        )
        self.request_by_employee_no_company = MagicMock(user=self.employee_no_company)

        self.employee_company2 = EmployeeFactory(
            is_active=True, company=self.company2
        )

    def test_has_object_permission(self):
        self.assertTrue(
            self.permission.has_object_permission(self.request_by_employee, self.view, self.employee_company))

        self.assertFalse(
            self.permission.has_object_permission(self.request_by_employee, self.view, self.employee_company2)
        )

    def test_has_permission(self):
        self.assertTrue(
            self.permission.has_permission(self.request_by_employee, self.view))

        self.assertFalse(
            self.permission.has_permission(self.request_by_employee_no_company, self.view))


class TestIsCompanyOwner(PermissionTest):
    def setUp(self):
        super().setUp()
        self.permission = IsCompanyOwner()
        self.company_owner = EmployeeFactory(
            is_active=True, is_company_owner=True, company=self.company
        )
        self.request_by_company_owner = MagicMock(user=self.company_owner)

    def test_has_object_permission(self):
        self.assertTrue(
            self.permission.has_object_permission(self.request_by_company_owner, self.view, self.employee_company))

        self.assertTrue(
            self.permission.has_object_permission(self.request_by_company_owner, self.view, self.company))

        self.assertFalse(
            self.permission.has_object_permission(self.request_by_company_owner, self.view, self.employee_company2)
        )

    def test_has_permission(self):
        self.assertTrue(
            self.permission.has_permission(self.request_by_company_owner, self.view))

        self.assertFalse(
            self.permission.has_permission(self.request_by_employee, self.view)
        )


class TestIsCompanyEmployeeOrAdmin(PermissionTest):
    def setUp(self):
        super().setUp()
        self.permission = IsCompanyEmployeeOrAdmin()

    def test_has_object_permission(self):
        self.assertTrue(
            self.permission.has_object_permission(self.request_by_admin, self.view, self.employee_company))

        self.assertTrue(
            self.permission.has_object_permission(self.request_by_admin, self.view, self.company))

        self.assertTrue(
            self.permission.has_object_permission(self.request_by_employee, self.view, self.employee_company2)
        )

    def test_has_permission(self):
        self.assertTrue(
            self.permission.has_permission(self.request_by_admin, self.view))

        self.assertTrue(
            self.permission.has_permission(self.request_by_employee, self.view)
        )
