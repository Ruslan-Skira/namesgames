from django.test import TestCase

from company.tests.factories.UserFactory import UserFactory


class BaseTestCase(TestCase):

    def setUp(self):
        self.staff = UserFactory(is_staff=True, is_active=True)

