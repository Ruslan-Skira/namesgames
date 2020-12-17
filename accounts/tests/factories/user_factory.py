import factory
from faker import Factory, Faker

faker = Factory.create()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Test function for creating fake users
    """

    class Meta:
        model = 'accounts.User'
        django_get_or_create = (
            'first_name',
            'last_name',
            'picture_url',
            'position',
            'birthday',
            'email',
            'phone_number',
            'skype',
            'company'
        )

    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.last_name())
    position = factory.LazyFunction(lambda: faker.job())
    picture_url = factory.LazyFunction(lambda: faker.url())
    birthday = factory.LazyFunction(lambda: faker.date_of_birth())
    email = factory.LazyFunction(lambda: faker.email())
    phone_number = factory.LazyFunction(lambda: faker.phone_number()[:17])
    skype = factory.LazyFunction(lambda: faker.word())
