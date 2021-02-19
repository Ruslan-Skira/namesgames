import datetime

from rest_framework import status
from rest_framework.settings import settings
from rest_framework.test import APIClient

from accounts.models import User
from accounts.tests.factories.user_factory import EmployeeFactory
from company.tests.base import BaseTestCase
from company.tests.factories.company_factory import CompanyFactory
from employees.serializers import EmployeeSerializer

client = APIClient()


class EmployeeByCompanyTest(BaseTestCase):
    """Test module for GET all companies API"""

    def setUp(self):
        """
        Creating set of Users and Companies before each test.
        """
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI2", last_parsed_at=datetime.datetime.today()
        )
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company2 = EmployeeFactory(
            is_active=True, company=self.test_company2
        )
        [EmployeeFactory(is_active=True, company=self.test_company) for _ in range(20)]

    def test_get_employees_by_company_valid(self):
        client.force_login(self.employee_test_company2)

        response = client.get(
            f"/api/v1/employees/by_company/{self.test_company2.slug}/", format="json"
        )

        self.assertEqual(
            response.json()["results"][0],
            EmployeeSerializer(self.employee_test_company2).data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_by_company_not_valid_company_slug(self):
        client.force_login(self.staff)
        response = client.get("/api/v1/employees/by_company/not-valid-testcompanyapi/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_by_company_not_authorized_user(self):
        response = client.get(f"/api/v1/employees/by_company/{self.test_company.slug}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # employees endpoint

    def test_employee_company_slug_unauthorized(self):
        response = client.get(f"/api/v1/employees/?company={self.test_company2}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_company_slug_not_employee(self):
        client.force_login(self.employee_test_company)

        response = client.get(f"/api/v1/employees/?company={self.test_company2}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_employees_filter_company(self):
        client.force_login(self.company_owner)

        response = client.get(f"/api/v1/employees/?company={self.test_company2}/")
        self.assertEqual(len(response.json()["results"]), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        client.force_login(self.company_owner)
        response = client.get(f"/api/v1/employees/?company={self.test_company}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()["results"]), settings.REST_FRAMEWORK["PAGE_SIZE"]
        )


class EmployeesListTest(BaseTestCase):
    def setUp(self):
        """
        The set of employees and companies will be created before each test.
        """

        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company2 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company3 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "password1": "swordfish",
            "password2": "swordfish",
        }
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )

    def test_get_all_employees(self):
        """
        Test should check the GET response length of the list with users
        admin + companyOwner + 2test_employee = 4 users
        """
        client.force_login(self.company_owner)
        response = client.get(f"/api/v1/employees/")
        self.assertEqual(len(response.json()["results"]), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_employee(self):
        """
        Test GET one employee.
        """

        client.force_login(self.company_owner)
        response = client.get(f"/api/v1/employees/{self.employee_test_company1.id}/")

        self.assertEqual(response.data["email"], self.employee_test_company1.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_employees_not_valid(self):
        """
        Test GET should check negative test case.
        """
        response = client.get("/api/v1/employees/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "password1": "swordfish",
            "password2": "swordfish",
        }
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_company_owner = EmployeeFactory(
            is_active=True, company=self.test_company, is_company_owner=True
        )

    def test_create_user_by_staff(self):
        """
        Test POST should check admin shouldn't create Employees.
        """
        client.force_login(self.staff)

        response = client.post("/api/v1/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_by_company_owner(self):
        """
        Test check company owner create new user in his company.
        """
        client.force_login(self.test_company_owner)

        response = client.post("/api/v1/employees/", data=self.test_user_data)
        user = User.objects.get(id=response.data["id"])
        # self.assertGreaterEqual(
        #     list(response.data.items()), list(user.items())
        # )
        assert response.data["email"] == user.email
        assert response.data["company"] == user.company_id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_users_not_valid(self):
        """
        Test POST with not valid user.
        """
        response = client.post("/api/v1/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_users_by_employee(self):
        """
        Test POST with authenticated user.
        """
        client.force_login(self.employee_test_company1)

        response = client.post("/api/v1/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeUpdateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "skype": "test3Skype",
            "position": "employee1",
        }

    def test_update_user(self):
        client.force_login(self.test_company_owner)
        """
        Test UPDATE should check how admin could update Employee.
        """

        response = client.put(
            f"/api/v1/employees/{self.employee_test_company.id}/",
            data=self.test_user_data,
        )
        self.assertGreaterEqual(
            list(response.data.items()), list(self.test_user_data.items())
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_by_company_owner(self):
        client.force_login(self.test_company_owner)
        """
        Test UPDATE user by Company Owner.
        """

        response = client.put(
            f"/api/v1/employees/{self.employee_test_company.id}/",
            data=self.test_user_data,
        )
        self.assertGreaterEqual(
            list(response.data.items()), list(self.test_user_data.items())
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_not_valid(self):
        """
        Test UPDATE should return 403 because user not allowed to do update.
        """

        response = client.put(
            f"/api/v1/employees/{self.employee_test_company.id}/",
            data=self.test_user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_by_employee(self):
        """
        Test UPDATE should return 403 because user not allowed to do update.
        """
        client.force_login(self.employee_test_company1)

        response = client.put(
            f"/api/v1/employees/{self.employee_test_company.id}/",
            data=self.test_user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EmployeeDeleteTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_company_owner = EmployeeFactory(
            is_active=True, company=self.test_company, is_company_owner=True
        )

    def test_delete_user(self):
        client.force_login(self.staff)
        """
        Test should check how admin couldn't delete Employee because he has his endpoint.
        """
        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_by_company_owner(self):
        client.force_login(self.test_company_owner)
        """
        Test DELETE should check how company owner could delete Employee in his company.
        """
        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")

        with self.assertRaisesMessage(
                User.DoesNotExist, "User matching query does not exist."
        ):
            User.objects.get(email=self.employee_test_company.email)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_not_valid(self):
        """
        Not authorized user shouldn't be able to delete any user.
        """
        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_by_employee(self):
        """
        Employee of any companies should not be able to delete any user .
        """
        client.force_login(self.employee_test_company1)

        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminListTest(BaseTestCase):
    def setUp(self):
        """
        The set of employees and companies will be created before each test.
        """

        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company2 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.employee_test_company3 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "password1": "swordfish",
            "password2": "swordfish",
        }
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )

    def test_get_all_employees(self):
        """
        Test should check the GET response length of the list with users
        admin + companyOwner + 2test_employee = 4 users
        """
        client.force_login(self.staff)
        response = client.get(f"/api/v1/admin/employees/")
        self.assertEqual(len(response.json()["results"]), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_employee(self):
        """
        Test GET one employee.
        """

        client.force_login(self.staff)
        response = client.get(f"/api/v1/admin/employees/{self.employee_test_company1.id}/")

        self.assertEqual(response.data["email"], self.employee_test_company1.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_employees_not_valid(self):
        """
        Test GET should check negative test case.
        """
        response = client.get("/api/v1/admin/employees/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "password": "swordfish",
        }

        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_user_data_company = {
            "email": "test_user_3@user.com",
            "company": self.test_company.id,
            "password": "swordfish",
            # "password2": "swordfish",
        }
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_company_owner = EmployeeFactory(
            is_active=True, company=self.test_company, is_company_owner=True
        )

    def test_create_user_by_staff(self):
        """
        Test POST should check admin shouldn't create Employees on company employee endpoint.
        """
        client.force_login(self.staff)

        response = client.post("/api/v1/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_no_company(self):
        """
        Test check admin create new user without company.
        """
        client.force_login(self.staff)

        response = client.post("/api/v1/admin/employees/", data=self.test_user_data)

        user = User.objects.get(email=response.data["email"])

        assert response.data["email"] == user.email
        assert response.data["company"] == user.company_id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_company(self):
        """
        Test check admin create new user in his company.
        """
        client.force_login(self.staff)

        response = client.post("/api/v1/admin/employees/", data=self.test_user_data_company)

        user = User.objects.get(id=response.data["id"])

        assert response.data["email"] == user.email

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_users_not_valid(self):
        """
        Test POST with not valid user.
        """
        response = client.post("/api/v1/admin/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_users_by_employee(self):
        """
        Test POST with authenticated user.
        """
        client.force_login(self.employee_test_company1)

        response = client.post("/api/v1/admin/employees/", data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUpdateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company1 = EmployeeFactory(
            is_active=True, company=self.test_company
        )
        self.test_user_data = {
            "email": "test_user_3@user.com",
            "skype": "test3Skype",
            "position": "employee1",
            "password": 'swordfish',
        }

    def test_update_user(self):
        client.force_login(self.staff)
        """
        Test UPDATE should check how admin could update Employee.
        """

        response = client.put(
            f"/api/v1/admin/employees/{self.employee_test_company.id}/",
            data=self.test_user_data,
        )
        self.assertGreaterEqual(
            list(response.data.items()), list(self.test_user_data.items())
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
