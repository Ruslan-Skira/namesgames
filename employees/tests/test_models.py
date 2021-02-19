# TODO:
#  1. model test create User model with company and then delete it. Look the Company model employee_count field.
#  2. Create end to end test with. Registration user and check how the employee_counter updated in Company model.
#  3. Create tests for SoftDeletionModel.
from django.test import TestCase

from company.models import Company


class BaseClass(TestCase):
    def setUp(self) -> None:
        self.name = 'Soft delete Company'
        self.company1 = Company.objects.create(name=self.name)

    def test_soft_delete_company(self):
        self.assertIsNone(self.company1.deleted_at)
        self.company1.delete()
        company = Company.all_objects.get(slug=self.company1.slug)
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.name, self.company1.name)

    def test_hard_delete_company(self):
        self.assertIsNone(self.company1.deleted_at)
        company = Company.objects.get(slug=self.company1.slug)
        company.hard_delete()
        company_hard_delete = list(Company.all_objects.filter(slug=self.company1.slug))
        self.assertEqual(company_hard_delete, [])

