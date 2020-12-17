import factory
from faker import Factory, Faker

faker = Factory.create()
fake = Faker()


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Company'
        django_get_or_create = (
            'name',
            'last_parsed_at'
        )

    name = factory.Sequence(lambda n: fake.unique.name())
    last_parsed_at = faker.date_object()
