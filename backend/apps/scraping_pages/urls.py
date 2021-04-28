from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import PageViewSet, ScrapingAlgorithmStatusViewSet, ScrapingAlgorithmViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"algorithms", ScrapingAlgorithmViewSet, basename="algorithms")
router.register(
    r"algorithm_statuses", ScrapingAlgorithmStatusViewSet, basename="algorithm_statuses"
)
router.register(
    r"pages", PageViewSet, basename="pages"
)

urlpatterns = [
    url(r"^", include(router.urls)),
]