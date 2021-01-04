import factory
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "Agent %03d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'swordfish')



