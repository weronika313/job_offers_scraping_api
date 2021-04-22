import inspect

from django.test import TestCase
from apps.scraping.indeed_scraper import IndeedScraper


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
