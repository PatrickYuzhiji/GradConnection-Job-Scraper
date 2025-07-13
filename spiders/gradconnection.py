import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import scrapy
from scrapy.selector import Selector
from items import JobItem


class GradconnectionSpider(scrapy.Spider):
    name = "gradconnection"
    allowed_domains = ["au.gradconnection.com"]
    start_urls = ["https://au.gradconnection.com/jobs/computer-science/"]

    def parse(self, response):
        sel = Selector(response)
        number_phrase = sel.css(
            "div.new-jobs-options-alignment.landing-panel-content-header > div > div > div > h4"
        ).extract_first()
        # 1 - 20 of 113 results
        number = int(number_phrase.split(" ")[-2])
        print(number)
        page_number = number // 20 + 1
        for i in range(1, page_number + 1):
            url = response.url + "?page=" + str(i)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        job_list = sel.css("div.outer-container")
        for job in job_list:
            job_item = JobItem()
            job_item["title"] = job.css("h3::text").extract_first()
            job_item["company"] = job.css(
                "div.box-employer-name > a > p::text"
            ).extract_first()
            job_item["type"] = job.css("p.ellipsis-text-pargraph::text").extract_first()
            job_item["location"] = job.css("p.location-name::text").extract_first()
            job_item["deadline"] = job.css("span.closing-in::text").extract_first()
            job_item["link"] = (
                "https://au.gradconnection.com"
                + job.css("a.box-header-title::attr(href)").extract_first()
            )
            yield job_item
