from django.db import models
from apps.scraping_pages.models import Page
from apps.users.models import CustomUser as User


# Create your models here.
class SearchCriteria(models.Model):
    language = models.CharField()
    experience_level = models.CharField()
    city_name = models.CharField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return f"Search criteria: language: {self.language}, experience level: {self.experience_level}, localization: {self.city_name}, page: {self.page} "


class SearchResult(models.Model):
    output_data = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    search_criteria = models.ForeignKey(
        SearchCriteria, on_delete=models.CASCADE
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Search results on {self.created_at}"

