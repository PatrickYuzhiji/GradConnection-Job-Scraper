import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


import scrapy
from scrapy.selector import Selector
from job.items import JobItem


class ProspleSpider(scrapy.Spider):
    name = "prosple"
    allowed_domains = ["au.prosple.com"]
    start_urls = [
        "https://au.prosple.com/search-jobs?study_fields=502&locations=9692&defaults_applied=1&work_rights=29062%2C29061%2C29063"
    ]

    def parse(self, response):
        sel = Selector(response)
        # "#__next > div > section > main > div > div > div > div > div > div > div > p"
        number_phrase = sel.css(
            "p.SearchResultCount__ResultsCount-sc-17kyq0v-0 bEIzsi"
        ).extract_first()
        # 1 - 20 of 113 results
        number = int(number_phrase.split(" ")[-2])
        print(number)
        page_number = number // 20 + 1
        for i in range(page_number):
            url = response.url + "&start=" + str(i * 20)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        job_list = sel.css(
            "#__next > div > section > main > div> div> div > div > ul > li.SearchResultsstyle__SearchResult-sc-c560t5-1"
        )

        for job in job_list:
            job_item = JobItem()
            job_item["title"] = job.css(
                "h2.JobTeaserstyle__JobTeaserTitle-sc-18thvj0-0::text"
            ).extract_first()
            job_item["company"] = job.css(
                "p.JobTeaserstyle__JobTeaserEmployerTitle-sc-18thvj0-5::text"
            ).extract_first()
            # job_item["type"] = job.css("p.ellipsis-text-pargraph::text").extract_first()
            # job_item["location"] = job.css("p.location-name::text").extract_first()
            # job_item["deadline"] = job.css("span.closing-in::text").extract_first()
            # job_item["link"] = (
            #     "https://au.gradconnection.com"
            #     + job.css("a.box-header-title::attr(href)").extract_first()
            # )
            yield job_item
