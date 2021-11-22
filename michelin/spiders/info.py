import os
from typing import List
import random

import scrapy
from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import (
    SplashRequest,
    SlotPolicy,
)
import pandas as pd

from michelin.items import InfoItem


class InfoSpider(scrapy.Spider):
    name = "info"
    BASE_DIR = "./data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_google_request_url(self, address: List[str]) -> str:
        search_query = "+".join(address)
        return f"https://google.com/search?q={search_query}"

    def create_naver_request_url(self, address: List[str]) -> str:
        search_query = "+".join(address)
        return f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={search_query}"

    def create_daum_request_url(self, address: List[str]) -> str:
        search_query = "+".join(address)
        return f"https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q={search_query}"

    def start_requests(self) -> None:
        target_city = self.city
        target_file_name = self.index
        df = pd.read_json(os.path.join(self.BASE_DIR, target_city, target_file_name))

        for i, row in df.iterrows():
            location = row["location"].split()
            title = row["title"].split()
            # address = location + title
            address = location[-1:] + title

            if i % 2 == 0:
                url = self.create_naver_request_url(address)
                engine = "naver"
                ports = [8051, 8053]
                port = random.choice(ports)
            else:
                url = self.create_daum_request_url(address)
                engine = "daum"
                port = [8050, 8052]
                port = random.choice(ports)

            yield SplashRequest(
                url,
                self.parse,
                args={
                    "wait": 1,
                },
                splash_url= f"http://192.168.42.186:{port}",
                meta={"location": location, "title": row["title"], "engine": engine},
            )

    def parse(self, response):

        name = response.meta["title"]
        # print("#################")
        if response.meta["engine"] == "naver":
            # crawl from naver
            selector = (
                "#main_pack > section.sc_new.sp_nreview._prs_rvw._au_view_collection"
            )
            result = response.css(selector)
            cadidates = result.css("div.total_wrap > div.total_area > a::attr(href)").getall()
        else:
            # crawl from daum
            selector = "#blogColl"
            result = response.css(selector)
            # print(result.css("div.cont_inner > div.wrap_tit  > a::attr(href)").getall())
            cadidates = result.css("div.cont_inner > div.wrap_tit  > a::attr(href)").getall()
        # print("#################")

        item = InfoItem()

        location = response.meta["location"]
        item["title"] = location[-2]
        item["category"] = location[-1]
        item["name"] = name
        item["candidates"] = cadidates[:5]

        yield item
