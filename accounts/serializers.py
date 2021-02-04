from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from accounts.models import User


class EmployeeRegisterSerializer(RegisterSerializer):
    """
    Serializer for registration with email
    """

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "password1": self.validated_data.get("password1"),
            "email": self.validated_data.get("email"),
        }


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer user querysets.
    """

    class Meta:
        model = User
        company = serializers.HyperlinkedIdentityField(view_name="company:user-detail")
        id = serializers.ReadOnlyField(label="ID", read_only=True)
        fields = [
            "first_name",
            "last_name",
            "picture_url",
            "position",
            "birthday",
            "email",
            "phone_number",
            "skype",
            "company",
            "id",
        ]


class AdminEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer Admin Employees querysets.
    """

    ...
