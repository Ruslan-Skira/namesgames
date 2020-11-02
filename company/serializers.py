from rest_framework import serializers

from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # company = serializers.HyperlinkedIdentityField(view_name="company:user-detail")
        fields = [
            'last_name',
            'picture_url',
            'position',
            'profile_url',
            'birthday',
            'email',
            'phone_number',
            'skype',
            'company'
        ]


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name',
            'slug',
            'last_parsed_at'
        ]
