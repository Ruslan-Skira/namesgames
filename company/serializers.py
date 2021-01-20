from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        slug = serializers.ReadOnlyField(label='Slug', read_only=True)

        fields = [
            'name',
            'slug',
            'last_parsed_at'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

        # TODO: read-only fields (slug) creation company. Test it
