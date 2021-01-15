from django.test import TestCase
from rest_framework.test import APITestCase

from accounts.tests.factories.user_factory import EmployeeFactory


class BaseTestCase(APITestCase):

    def setUp(self):
        self.staff = EmployeeFactory(is_staff=True, is_active=True)
