import inspect

from django.test import TestCase
from apps.scraping.scraping_algorithms.indeed_scraper import IndeedScraper
from apps.scraping.registry import ScrapingRegistry


class ScrapeTests(TestCase):
    def test_indeed_scraper_algorithm(self):
        input_data = {
            "search_criteria":
                {
                    'language': 'Python',
                    'experience_level': 'Junior',
                    'location': 'Białystok'

                },
            "number_of_pages": 3
        }
        scraper = IndeedScraper()
        response = scraper.get_job_offers(input_data)

        self.assertEqual("OK", response["status"])
        self.assertTrue("job_offers" in response)


    def test_registry(self):
        registry = ScrapingRegistry()
        self.assertEqual(len(registry.pages), 0)
        page_name = "indeed"
        page_url = "https://pl.indeed.com/"
        algorithm_object = IndeedScraper
        algorithm_name = "scraping job offers from indeed"
        algorithm_status = "production"
        algorithm_version = "v1"
        algorithm_description = (
            "after receiving the search criterion, the algorithm returns job offers containing the title, the time of "
            "addition, description, link, company name and information about the possibility of remote work "
        )
        algorithm_code = inspect.getsource(IndeedScraper)
        # add to registry
        registry.add_algorithm(
            page_name,
            page_url,
            algorithm_object,
            algorithm_name,
            algorithm_status,
            algorithm_version,
            algorithm_description,
            algorithm_code,
        )
        # there should be one endpoint available
        self.assertEqual(len(registry.pages), 1)
