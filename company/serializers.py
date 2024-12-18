from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company

        fields = ["name", "slug", "last_parsed_at"]
        read_only_fields = ["slug"]
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}
