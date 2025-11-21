import scrapy
from datetime import datetime

class HKCSIPSpider(scrapy.Spider):
    name = "hk_csip"
    allowed_domains = ["cybersecurity.hk"]
    start_urls = [
        "https://www.cybersecurity.hk/en/index.php"
    ]

    def parse(self, response):
        self.logger.info(f"Parsing index page: {response.url}")
        # Follow links to Expert Corner and Learning Centre articles
        links = response.css("a::attr(href)").getall()
        self.logger.info(f"Found {len(links)} links on index page.")
        
        for href in links:
            if "expert-" in href or "learning-" in href:
                self.logger.info(f"Following link: {href}")
                yield response.follow(href, self.parse_article)

    def parse_article(self, response):
        self.logger.info(f"Parsing article: {response.url}")
        # Try multiple title selectors
        title = response.css("h1.page-title::text").get()
        if not title:
            title = response.css("div.content-area h2::text").get()
        if not title:
            title = response.css("h2::text").get()
            
        date = response.css("span.date::text").get()
        
        # Get all text from content area, join and clean
        content_list = response.css("div.content-area *::text").getall()
        if not content_list:
             content_list = response.css("div#main_content *::text").getall()
        
        # Fallback: get all body text if specific areas fail
        if not content_list:
            content_list = response.css("body *::text").getall()

        content = " ".join(content_list).strip()
        content = " ".join(content.split())

        self.logger.info(f"Extracted Title: {title}")
        self.logger.info(f"Extracted Content Length: {len(content)}")

        if title and content:
            yield {
                "region": "HK",
                "source_url": response.url,
                "title": title.strip(),
                "content_block": content,
                "published_date": date.strip() if date else None,
                "scraped_at": datetime.now().isoformat()
            }
        else:
            self.logger.warning(f"Failed to extract title or content from {response.url}")
