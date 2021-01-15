import datetime

from django.test import TestCase

from accounts.models import User
from company.models import Company


class CompanyTest(TestCase):
    """Test model for Company model"""

    def setUp(self):
        test_company = Company.objects.create(
            name='TestCompanyModel1', last_parsed_at=datetime.datetime.today())
        User.objects.create(
            first_name='test_name', last_name='test_last_name', picture_url='http://fakeurl', position='test_position',
            birthday=datetime.date(2000, 12, 1), email='example@test.com', phone_number='+3809877612', skype='test',
            company=test_company)

    def test_company_employee(self):
        company_test = Company.objects.get(name='TestCompanyModel1')
        employee_test = User.objects.get(company=company_test)
        self.assertEqual(company_test.name, 'TestCompanyModel1')
        self.assertEqual(employee_test.first_name, 'test_name')
