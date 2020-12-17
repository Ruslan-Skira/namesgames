from django.contrib.auth import get_user_model
from django.test import TestCase


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
        self.assertTrue(admin_user.is_company_owner)
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