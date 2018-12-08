import scrapy
from bookspider.items import Book

class BookSpider(scrapy.Spider):
  start_urls = [
    'http://books.toscrape.com/catalogue/category/books/romance_8/page-1.html',
    'http://books.toscrape.com/catalogue/category/books/romance_8/page-2.html'
  ]
  name = 'book'

  def parse(self, response):
    print("##########################################################################################")
    for book in response.css('li article.product_pod'):
      href = book.css('a::attr(href)').extract_first()
      full_url = response.urljoin(href)
      
      yield scrapy.Request(full_url, callback=self.parse_book)

  def parse_book(self, response):
    title = response.css('h1::text').extract_first()
    description = response.css('.product_page > p::text').extract()
    src = response.css('.product_page .thumbnail img::attr(src)').extract_first()
    cover = response.urljoin(src)

    yield Book(title=title, description=description, file_urls=[cover])