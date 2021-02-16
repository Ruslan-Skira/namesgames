from rest_framework import serializers

from accounts.models import User


class AdminEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer Admin Employees querysets.
    """

    class Meta:
        model = User
        company = serializers.HyperlinkedIdentityField(view_name="company:user-detail", read_only=False)
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
