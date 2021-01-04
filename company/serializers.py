from rest_framework import serializers

from accounts.models import User
from .models import Company


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        company = serializers.HyperlinkedIdentityField(view_name="company:user-detail")
        fields = [
            'last_name',
            'picture_url',
            'position',
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
        # TODO here was todo to know for what does it need? slug
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
