import scrapy
from datetime import datetime

class NYCCyberSpider(scrapy.Spider):
    name = "nyc_cyber"
    allowed_domains = ["nyc.gov"]
    start_urls = [
        "https://www1.nyc.gov/content/oti/pages/cybersecurity.html"
    ]

    def parse(self, response):
        self.logger.info(f"Parsing NYC OTI cybersecurity page: {response.url}")
        
        # Extract main content sections
        # NYC OTI pages typically have content in specific divs
        main_content = response.css("div.main-content, div.content-area, article")
        
        if main_content:
            title = response.css("h1::text, title::text").get() or "NYC Cybersecurity Information"
            content_parts = main_content.css("*::text").getall()
            content = " ".join(content_parts).strip()
            content = " ".join(content.split())  # Clean whitespace
            
            if content and len(content) > 100:
                yield {
                    "region": "NYC",
                    "source_url": response.url,
                    "title": title.strip(),
                    "content_block": content,
                    "published_date": None,
                    "scraped_at": datetime.now().isoformat()
                }
        
        # Follow links to cybersecurity-related pages
        links = response.css("a::attr(href)").getall()
        for href in links:
            if any(keyword in href.lower() for keyword in ['cyber', 'security', 'privacy', 'data-protection']):
                self.logger.info(f"Following cybersecurity link: {href}")
                yield response.follow(href, self.parse_article)
    
    def parse_article(self, response):
        self.logger.info(f"Parsing NYC article: {response.url}")
        
        title = response.css("h1::text").get()
        if not title:
            title = response.css("title::text").get()
        
        # Get main content
        content_list = response.css("div.main-content *::text, div.content-area *::text, article *::text").getall()
        if not content_list:
            content_list = response.css("body *::text").getall()
        
        content = " ".join(content_list).strip()
        content = " ".join(content.split())
        
        if title and content and len(content) > 100:
            yield {
                "region": "NYC",
                "source_url": response.url,
                "title": title.strip(),
                "content_block": content,
                "published_date": None,
                "scraped_at": datetime.now().isoformat()
            }
