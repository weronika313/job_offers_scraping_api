from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ScrapingAlgorithm(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' from page ' + self.page.name


class ScrapingAlgorithmStatus(models.Model):
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_algorithm = models.ForeignKey(
        ScrapingAlgorithm, on_delete=models.CASCADE, related_name="status"
    )

    def __str__(self):
        return self.parent_algorithm.name + ' ' + self.status
