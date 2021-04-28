from django.db import transaction
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from .models import Page, ScrapingAlgorithm, ScrapingAlgorithmStatus
from .serializers import PageSerializer, ScrapingAlgorithmSerializer, ScrapingAlgorithmStatusSerializer


class PageViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class ScrapingAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = ScrapingAlgorithmSerializer
    queryset = ScrapingAlgorithm.objects.all()


def deactivate_old_statuses(instance):
    old_statuses = ScrapingAlgorithmStatus.objects.filter(
        parent_mlalgorithm=instance.parent_mlalgorithm,
        created_at__lt=instance.created_at,
        active=True,
    )
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    ScrapingAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])


class ScrapingAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    permission_classes = (AllowAny,)
    serializer_class = ScrapingAlgorithmStatusSerializer
    queryset = ScrapingAlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_old_statuses(instance)

        except Exception as e:
            raise APIException(str(e))
