import math
import re

import requests
from bs4 import BeautifulSoup


class IndeedScraper:
    def __init__(self):
        self.base_url = 'https://pl.indeed.com'
        self.posts_per_page = 15

    def transform_search_criteria(self, search_criteria: dict):
        search_criteria.update((key, value.replace(' ', '+')) for key, value in search_criteria.items())
        return search_criteria

    def load_page(self, page_url):
        page = requests.get(page_url)
        if not page:
            return None

        soup = BeautifulSoup(page.text, "html.parser")

        return soup

    def find_total_number_of_pages(self, soup):
        pages = soup.find(id="searchCountPages")
        if not pages:
            return 0
        text = pages.text.strip()
        number_of_results = int(re.findall(r"\d+", text)[1])
        return math.ceil(number_of_results / self.posts_per_page)

    def prepare_url(self, search_criteria: dict):
        language, experience_level, city_name = search_criteria.values()
        page_url = (
            f'{self.base_url}'
            '/praca?'
            f'q={experience_level}+{language}&'
            f'l={city_name}'
        )
        return page_url

    def scrape_job_offers(self, user_number_of_pages, search_criteria):
        job_offers = []
        url_to_scrape = self.prepare_url(search_criteria)
        number_of_pages = self.swap_if_user_number_of_pages_is_greater_than_total(user_number_of_pages,
                                                                                         url_to_scrape)
        offers_per_page = self.get_offers_per_page(number_of_pages)
        for i in offers_per_page:
            extension = ""
            if i != 0:
                extension = "&start=" + str(i)
            url = url_to_scrape + extension
            soup = self.load_page(url)
            job_soup = soup.find(id="resultsCol")
            job_offers = self.get_offers_from_webpage(job_offers, job_soup)

        return job_offers

    def swap_if_user_number_of_pages_is_greater_than_total(self, user_number_of_pages, url):
        soup = self.load_page(url)
        total_number_of_pages = self.find_total_number_of_pages(soup)
        number_of_pages = user_number_of_pages if user_number_of_pages < total_number_of_pages else total_number_of_pages
        return number_of_pages

    def get_offers_from_webpage(self, job_offers, job_soup):
        for div in job_soup.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result"):
            job_offer = self.extract_data_points(div)
            job_offers.append(job_offer)
        return job_offers

    def extract_data_points(self, div):
        job_offer = {}

        for a in div.findAll('a', attrs={'class': 'jobtitle turnstileLink'}):
            try:
                job_offer['title'] = a['title']
            except TypeError:
                job_offer['title'] = 'Unknown'

            try:
                job_offer['link']= self.base_url + a['href']
            except TypeError:
                job_offer['link'] = 'Unknown'

        for a1 in div.findAll('a', attrs={'data-tn-element': 'companyName'}):
            try:
                job_offer['company_name'] = a1.text.strip()
            except TypeError:
                job_offer['company_name'] = 'Unknown'

        for span in div.findAll('span', attrs={'class': 'location accessible-contrast-color-location'}):
            try:
                job_offer['location'] = span.text.strip()
            except TypeError:
                job_offer['location'] = 'Unknown'

        for div1 in div.findAll('div', attrs={'class': 'summary'}):
            try:
                summary = div1.text.strip()
                job_offer['summary'] = re.sub(' +', ' ', summary.replace("\n", " "))
            except TypeError:
                job_offer['summary'] = 'Unknown'

        for span1 in div.findAll('span', attrs={'class': 'date'}):
            try:
                job_offer['date'] = span1.text.strip()
            except TypeError:
                job_offer['date'] = 'Unknown'

        for span3 in div.findAll('span', attrs={'class': 'remote'}):
            job_offer['remote'] = span3.text.strip()

        return job_offer

    def get_offers_per_page(self, number_of_pages):
        return [i for i in range(0, number_of_pages * 10, 10)]

    def postprocessing(self, job_offers):
        return {"job_offers": job_offers, "status": "OK"}

    def get_job_offers(self, input_data: dict):
        try:
            search_criteria = input_data.get("search_criteria")
            user_number_of_pages = input_data.get("number_of_pages")
            search_criteria = self.transform_search_criteria(search_criteria)
            job_offers = self.scrape_job_offers(user_number_of_pages, search_criteria)
            job_offers = self.postprocessing(job_offers)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return job_offers