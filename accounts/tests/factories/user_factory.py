import factory
from django.contrib.auth import get_user_model
from faker import Factory
from faker import Faker

faker = Factory.create()
fake = Faker()


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Test function for creating fake users
    """

    class Meta:
        model = get_user_model()

    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.last_name())
    position = factory.LazyFunction(lambda: faker.job())
    picture_url = factory.LazyFunction(lambda: faker.url())
    birthday = factory.LazyFunction(lambda: faker.date_of_birth())
    email = factory.LazyFunction(lambda: faker.email())
    phone_number = factory.LazyFunction(lambda: faker.phone_number()[:17])
    skype = factory.LazyFunction(lambda: faker.word())
    password = factory.PostGenerationMethodCall('set_password', 'swordfish')

    is_active = True
