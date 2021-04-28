from rest_framework import serializers
from backend.apps.scraping_pages.models import ScrapingAlgorithm
from backend.apps.scraping_pages.models import ScrapingAlgorithmStatus
from backend.apps.scraping_pages.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        read_only_fields = ("id", "name", "url")
        fields = read_only_fields


class ScrapingAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, algorithm):
        return (
            ScrapingAlgorithmStatus.objects.filter(parent_algorithm=algorithm)
                .latest("created_at")
                .status
        )

    class Meta:
        model = ScrapingAlgorithm
        read_only_fields = (
            "id",
            "name",
            "description",
            "code",
            "version",
            "created_at",
            "page",
            "current_status",
        )
        fields = read_only_fields


class ScrapingAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_at", "parent_algorithm")
