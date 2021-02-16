import datetime

from dictdiffer import diff
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import settings
from rest_framework.test import APIClient

from accounts.models import User
from employees.serializers import EmployeeSerializer
from accounts.tests.factories.user_factory import EmployeeFactory
from company.models import Company
from company.serializers import CompanySerializer
from company.tests.base import BaseTestCase
from company.tests.factories.company_factory import CompanyFactory
from company.tests.utils.dict_without_keys import dict_without_keys

client = APIClient()


class CompanyCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.test_company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_create_company_is_staff(self):
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

    def test_create_company_is_not_staff(self):
        """
        Tests not staff create company and check it.
        """
        data = {
            "name": "Test company 4",
        }
        response = client.post(reverse("companies-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CompanyListTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_get_all_companies(self):
        response = client.get(reverse("companies-list"))
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanyRetrieveTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_get_one_company(self):
        response = client.get(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug})
        )
        data = {
            "name": self.test_company.name,
            "slug": self.test_company.slug,
        }
        assert (
                list(
                    diff(
                        dict_without_keys(response.data, ["last_parsed_at"]),
                        dict_without_keys(data, []),
                    )
                )
                == []
        )
        self.assertGreaterEqual(response.data.items(), data.items())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_company_invalid_slug(self):
        response = client.get(
            reverse(
                "companies-detail",
                kwargs={"slug": self.test_company.slug + "invalidslug"},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CompanyUpdateTest(BaseTestCase):
    def setUp(self):
        ContentType.objects.clear_cache()
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_update_company(self):
        client.force_login(self.company_owner)
        data = {"name": "updated company", "slug": "updated-company"}
        response = client.put(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug}),
            data=data,
        )

        self.assertGreaterEqual(response.data.items(), data.items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_not_authorized_user(self):
        data = {"name": "updated company", "slug": "updated-company"}
        response = client.put(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_another_company_employee(self):
        client.force_login(self.employee_test_company)
        data = {"name": "updated company", "slug": "updated-company"}
        response = client.put(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug}),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CompanyDeleteTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_company = CompanyFactory(
            name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
        )
        self.test_company2 = CompanyFactory(
            name="TestCompanyAPI-2", last_parsed_at=datetime.datetime.today()
        )

        self.staff = EmployeeFactory(is_staff=True, is_active=True)
        self.company_owner = EmployeeFactory(
            is_company_owner=True, is_active=True, company=self.test_company
        )
        self.employee_test_company = EmployeeFactory(
            is_active=True, company=self.test_company
        )

    def test_delete_company(self):
        client.force_login(self.staff)

        response = client.delete(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_company_not_valid(self):
        response = client.delete(
            reverse("companies-detail", kwargs={"slug": self.test_company.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
        client.force_login(self.staff)

        response = client.get(f"/api/v1/employees/?company={self.test_company2}/")
        self.assertEqual(len(response.json()["results"]), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        client.force_login(self.staff)
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

    def test_get_all_employees(self):
        """
        Test should check the GET response length of the list with users
        admin + companyOwner + 2test_employee = 4 users
        """
        client.force_login(self.staff)
        response = client.get(f"/api/v1/employees/")
        self.assertEqual(len(response.json()["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_employee(self):
        client.force_login(self.staff)
        """
        Test GET one employee.
        """

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
        client.force_login(self.staff)
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
        Test DELETE should check how admin could delete Employee.
        """
        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")

        with self.assertRaisesMessage(
                User.DoesNotExist, "User matching query does not exist."
        ):
            User.objects.get(id=self.employee_test_company.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_not_valid(self):
        """
        Not authorized user shouldn't be able to delete any user.
        """
        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_by_employee(self):
        """
        Employee of any companies should be able to delete any user .
        """
        client.force_login(self.employee_test_company1)

        response = client.delete(f"/api/v1/employees/{self.employee_test_company.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# class AdminEmployeeCreateTest(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.test_user_data = {
#             "email": "test_user_3@user.com",
#             "password1": "swordfish",
#             "password2": "swordfish",
#         }
#         self.test_company = CompanyFactory(
#             name="TestCompanyAPI-1", last_parsed_at=datetime.datetime.today()
#         )
#         self.employee_test_company1 = EmployeeFactory(
#             is_active=True, company=self.test_company
#         )
#         self.test_company_owner = EmployeeFactory(
#             is_active=True, company=self.test_company, is_company_owner=True
#         )
#
#     @skip
#     def test_create_employee(self):
#         """
#         Test check how Admin could create employee.
#         """
#         client.force_login(self.staff)
#
#         response = client.post("/api/v1/admin/employees/", data=self.test_user_data)
#         user_db = User.objects.get(email=self.test_user_data['email'])
#         self.assertGreaterEqual(
#             list(response.data.items()), list(user_db.items())
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
