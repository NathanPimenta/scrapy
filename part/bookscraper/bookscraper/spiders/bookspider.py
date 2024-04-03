import scrapy
class BookspiderSpider(scrapy.Spider): #Define the spider class
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]  #having this prevents scraping from all connected websites
    start_urls = ["https://books.toscrape.com/"]
# after using fetch function in bash it stores everything in the response variable    
    

    def parse(self, response):           # parse function is called once response comes back
        book=response.css('article.product_pod')          #the parse functions selects all the books form the response that come under article tag with product_pod as class name
        for item in book:                    #Iterate over each book element
            yield{
                'Name': item.css('h3 a::text').get(),
                'Price':item.css('.product_price .price_color::text').get(),
                'url': item.css('h3 a').attrib['href']
            }
            next_page = response.css('li.next a::attr(href)').get()
     
        if next_page is not None:
    
            if 'catalogue/' in next_page:
                next_url = 'https://books.toscrape.com/'+next_page
            else:     
                next_url='https://books.toscrape.com/catalogue/'+next_page
# we use if statement to sort the bug where scraping stopped after page 2 and gave an http error
            yield response.follow(next_url, callback=self.parse) #we tell scrapy to go to the next page using response.follow
            #once response comes form url callback occurs and parse is done

#The yield keyword is used to return a generator object. This allows the spider to scrape multiple pages without having to wait for each page to load.

        
    
    