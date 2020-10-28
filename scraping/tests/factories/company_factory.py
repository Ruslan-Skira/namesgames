import factory
from faker import Factory, Faker

faker = Factory.create()
fake = Faker()


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'scraping.Company'
        django_get_or_create = (
            'name',
            'last_parced_at'
        )

    name = factory.Sequence(lambda n: fake.unique.name())
    last_parced_at = faker.date_object()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'scraping.Employee'
        django_get_or_create = (
            'first_name',
            'last_name',
            'picture_url',
            'position',
            'profile_url',
            'birthday',
            'email',
            'phone_number',
            'skype',
            'company'
        )

    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.last_name())
    picture_url = factory.LazyFunction(lambda: faker.url())
    position = factory.LazyFunction(lambda: faker.job())
    profile_url = factory.LazyFunction(lambda: faker.url())
    birthday = factory.LazyFunction(lambda: faker.date_of_birth())
    email = factory.LazyFunction(lambda: faker.email())
    phone_number = factory.LazyFunction(lambda: faker.phone_number()[:17])
    skype = factory.LazyFunction(lambda: faker.word())
    company = factory.SubFactory(CompanyFactory)
