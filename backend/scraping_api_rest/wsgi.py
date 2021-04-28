"""
WSGI config for scraping_api_rest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import inspect
from apps.scraping.registry import ScrapingRegistry
from apps.scraping.scraping_algorithms.indeed_scraper import IndeedScraper

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()

try:
    registry = ScrapingRegistry()  # create ML registry
    # Random Forest classifier
    rf = IndeedScraper()
    # add to ML registry
    registry.add_algorithm(
        page_name="indeed",
        page_url="https://pl.indeed.com/",
        algorithm_object=IndeedScraper,
        algorithm_name="scraping job offers from indeed",
        algorithm_status="production",
        algorithm_version="v1",
        algorithm_description=(
            "after receiving the search criterion, the algorithm returns job offers containing the title, the time of "
            "addition, description, link, company name and information about the possibility of remote work "
        ),
        algorithm_code=inspect.getsource(IndeedScraper))


except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
