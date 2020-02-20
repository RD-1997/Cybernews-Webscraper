import scrapy
import os
from scrapy.crawler import CrawlerProcess

# scrapes the latest cyber news from thehackernews.com
class hackerSpiderClass(scrapy.Spider):

    # name of spider
    name = "hackerSpider"

    # website to scrape from
    start_urls=[
        'https://thehackernews.com',
    ]

    def parse(self, response):

        # links to follow up and retrieve information from
        link = response.xpath(".//*[@class ='story-link']/@href").extract()

        # for each link in the list of links, follow up and continue parse_thread method
        for thread in link:

            yield response.follow(thread,self.parse_thread)


    def parse_thread(self, response):

        # retrieves the articles title
        title = response.xpath("//*[@class='story-title']/a/text()").extract_first()

        # retrieves the published date
        date = response.xpath("//*[@class='author']/text()").extract_first()

        # the website name
        website = 'https://thehackernews.com'

        yield{
            "website": website,
            "title": title,
            "date": date

        }

# scrapes the news from cyware.com
class cywareSpiderClass(scrapy.Spider):

    # name of crawler
    name = "cywareSpider"

    # website to crawl from
    start_urls=[
        'https://cyware.com/cyber-security-news-articles'
    ]

    def parse(self, response):

        # creates a list of the website's threads
        threads = response.xpath("//*[@class='post post-v2 format-image news-card get-id']").extract()

        # some variables to optimize scraping
        i = 0
        n = 0

        for thread in threads:

            # the website name
            website = "https://cyware.com"

            # retrieves the article's title
            title = response.xpath("//*[@class='post-title post-v2-title text-image']/a/text()").extract()[i]

            # retrieves the publish date of the article
            date = response.xpath("//*[@class='date']/text()").extract()[n]

            # creates a nice structure for the information that's being scraped
            yield{

                "website": website,
                "title": title,
                "date": date

            }

            # for scraping optimization
            i += 1
            n += 3

# removes the result.json file so a fresh one can be made
os.remove('../logs/result.json')

# stores the output of the spiders in a json file
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': '../logs/result.json'
})

# executes the spiders simultaneously
process.crawl(hackerSpiderClass)
process.crawl(cywareSpiderClass)
process.start()



