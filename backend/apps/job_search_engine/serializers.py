from rest_framework import serializers
from .models import SearchCriteria, SearchResult


class SearchCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchCriteria
        read_only_fields = ("language", "experience_level", "city_name", "page")
        fields = read_only_fields


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        read_only_fields = ("output_data", "created at", "search criteria", "user")
