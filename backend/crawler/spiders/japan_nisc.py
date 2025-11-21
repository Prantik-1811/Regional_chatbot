import scrapy
from datetime import datetime

class JapanNISCSpider(scrapy.Spider):
    name = "japan_nisc"
    allowed_domains = ["nisc.go.jp"]
    start_urls = [
        "https://www.nisc.go.jp/eng/"
    ]

    def parse(self, response):
        self.logger.info(f"Parsing NISC index page: {response.url}")
        
        # Extract PDF links from "What's new" section
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        self.logger.info(f"Found {len(pdf_links)} PDF links")
        
        for href in pdf_links:
            # Follow PDF links to extract metadata
            # For now, we'll just store the link info
            full_url = response.urljoin(href)
            
            # Extract title from nearby text
            # This is a simplified approach - in production, we'd parse more carefully
            title = href.split('/')[-1].replace('.pdf', '').replace('_', ' ')
            
            yield {
                "region": "JP",
                "source_url": full_url,
                "title": title,
                "content_block": f"Document available at: {full_url}",
                "published_date": None,
                "scraped_at": datetime.now().isoformat()
            }
        
        # Also extract text content from main sections
        sections = response.css("div.section")
        for section in sections:
            title = section.css("h3::text").get()
            content = " ".join(section.css("*::text").getall()).strip()
            
            if title and content and len(content) > 100:
                yield {
                    "region": "JP",
                    "source_url": response.url,
                    "title": title.strip(),
                    "content_block": " ".join(content.split()),
                    "published_date": None,
                    "scraped_at": datetime.now().isoformat()
                }
