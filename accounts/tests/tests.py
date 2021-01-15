from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase


class UsersManagersTests(TestCase):
    """
    User test cases.
    """

    def test_create_user(self):
        """
        Positive and negative test case during creating user.
        """
        User = get_user_model()
        user = User.objects.create_user(email='test1@user.com', password='test123')
        self.assertEqual(user.email, 'test1@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_company_owner)
        try:
            # user is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='123')

    def test_create_superuser(self):
        """
        Test create superuser for positive test case and negative testcases.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser('testadmin@user.com', 'admintest')
        self.assertEqual(admin_user.email, 'testadmin@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='testadmin@user.com',
                password='blabla',
                is_superuser=False
            )

class UsersAPITests(APITestCase):
    def test_registration_user(self):
        """
        Tests user could pass registration with email, password1, password2.
        """
    # TODO tests http://localhost:8080/auth/registration/
    #  1. Registration valid user
    #  2. Registration with the same user email
    #  3. Registration with not valid email
    ...

    def test_login_user(self):
        """
        Tests login user """
        ...
