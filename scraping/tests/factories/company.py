import random
import datetime
from django.utils.text import slugify
import factory
from faker import Factory
from faker import Faker

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
    last_name = faker.last_name()
    picture_url = faker.url()
    position = faker.job()
    profile_url = faker.url()
    birthday = faker.date_of_birth()
    email = faker.email()
    phone_number = faker.phone_number()[:17]
    skype = faker.word()
    company = factory.SubFactory(CompanyFactory)




