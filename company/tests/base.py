from django.test import TestCase
from rest_framework.test import APITestCase

from accounts.tests.factories.user_factory import EmployeeFactory


class BaseTestCase(APITestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.staff = EmployeeFactory(is_staff=True, is_active=True, is_superuser=True)
