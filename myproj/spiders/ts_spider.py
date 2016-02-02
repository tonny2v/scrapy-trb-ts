import scrapy
from ..items import MyprojItem
class trbSpider(scrapy.Spider):
    name = "trb"
    allowed_domains = ["sciencedirect.com"]
    start_urls = [
        "http://www.sciencedirect.com/science/journal/01912615",
    ]

    def parse(self, response):
        print '------ crawling root dir ------'
        for href in response.css('a.volLink::attr("href")'):
            url = response.urljoin(href.extract())
            print url
            yield scrapy.Request(url, self.parse_volume)

    def parse_volume(self, response):
        print '------ crawling sub dir ------'
        for href in response.css('div.currentVolumes a::attr("href")'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        print '------ crawing authors name'
        for authors in response.css('li.authors::text'):
            yield {'authors': authors.extract()}


class tsSpider(scrapy.Spider):

    name = "ts"
    allowed_domains = ["informs.org"]
    start_urls = [
        "http://pubsonline.informs.org/loi/trsc",
    ]

    # def start_requests(self):
    #     yield scrapy.Request("http://pubsonline.informs.org/loi/trsc",
    #                   headers={'User-Agent':
    #                   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    #                           "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"})

    def parse(self, response):
        print '------ crawling root dir ------'
        for href in response.css("div.row > a::attr('href')"):
            url = response.urljoin(href.extract())
            print url
            yield scrapy.Request(url, self.parse_volume)

    def parse_volume(self, response):
        print '------ crawling sub dir ------'
        # for href in response.css("span>:first-child.hlFld-ContribAuthor::text"):
        for authors in response.css("span.hlFld-ContribAuthor::text"):
            item = MyprojItem()
            item['author_name'] = authors.extract()
            yield item
