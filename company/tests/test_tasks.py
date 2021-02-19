import datetime

from django.test import TestCase

from accounts.models import User
from company.models import Company
from company.tasks import company_employees_counter


class CompanyEmployeesCounterTask(TestCase):
    def setUp(self) -> None:
        self.test_company = Company.objects.create(
            name="TestCompanyModel1", last_parsed_at=datetime.datetime.today()
        )
        self.test_user = User.objects.create(
            first_name="test_name",
            last_name="test_last_name",
            picture_url="http://fakeurl",
            position="test_position",
            birthday=datetime.date(2000, 12, 1),
            email="example@test.com",
            phone_number="+3809877612",
            skype="test",
            company=self.test_company,
        )

    def test_company_employees_counter(self):
        """
        Test check that company_employees_counter updates.
        """
        company_employees_counter(self.test_company.id)
        company_test = Company.objects.get(name="TestCompanyModel1")
        employee_test = User.objects.get(company=company_test)

        self.assertEqual(company_test.employees_count, 1)
        employee_test.delete()
        company_employees_counter(company_test.id)
        self.assertEqual(company_test.employees_count, 1)
