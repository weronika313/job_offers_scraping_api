from apps.scraping_pages.models import ScrapingAlgorithm
from apps.scraping_pages.models import ScrapingAlgorithmStatus
from apps.scraping_pages.models import Page


class ScrapingRegistry:
    def __init__(self):
        self.pages = {}

    def add_algorithm(
        self,
        page_name,
        page_url,
        algorithm_object,
        algorithm_name,
        algorithm_status,
        algorithm_version,
        algorithm_description,
        algorithm_code,
    ):

        page, _ = Page.objects.get_or_create(name=page_name, url=page_url)

        (
            database_object,
            algorithm_created,
        ) = ScrapingAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            page=page,
        )
        if algorithm_created:
            status = ScrapingAlgorithmStatus(
                status=algorithm_status, parent_algorithm=database_object, active=True
            )
            status.save()

        self.pages[database_object.id] = algorithm_object
