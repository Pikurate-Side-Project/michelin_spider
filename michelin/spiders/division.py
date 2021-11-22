import scrapy

from michelin.items import MichelinItem


class DivisionSpider(scrapy.Spider):
    name = "division"

    def convert_url(self, keyword: str, page: int) -> str:
        return (
            f"https://www.mangoplate.com/search/{keyword}?keyword={keyword}&page={page}"
        )

    def start_requests(self):
        with open("data/preprocess.tsv", "r") as f:
            lines = f.readlines()

        for line in lines:
            keyword = line.split()[-1]
            for i in range(30):
                url = self.convert_url(keyword, i + 1)
                yield scrapy.Request(url, callback=self.parse, meta={"location": line})

    def parse(self, response):
        titles = response.css("h2.title::text").getall()
        if not titles:
            return

        for title in titles:
            title = title.strip()
            if title:
                item = MichelinItem()
                item["location"] = response.meta["location"].strip()
                item["title"] = title
                yield item
