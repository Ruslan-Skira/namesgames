from rest_framework import serializers

from .models import Company, User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        # TODO: what for is it used? maybe not needed?
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
