import scrapy

# This spider enables me to crawl all the urls from steam.
class SteamtopsellSpider(scrapy.Spider):
    name = 'steamtopsell'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?category1=998&filter=topsellers&page=1']

    def parse(self, response):
        # restore all the game urls
        urls = response.xpath("//div[@id='search_resultsRows']/a/@href").extract()
        for url in urls:
            yield {
                'url': url
            }
        # find next page
        next_page = response.xpath("//div[@class='search_pagination_right']/child::a[last()]/@href").get()
        # print(next_page)
        # it contains 25 urls in one store.steampowered.com page
        # print(len(urls))

        if next_page is not None:
          
            yield response.follow(next_page, callback=self.parse)
