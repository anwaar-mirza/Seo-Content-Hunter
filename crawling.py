import json, asyncio, time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonXPathExtractionStrategy, CacheMode
from threading import Thread
import random
class WebCrawler:
    def __init__(self):
        self.schema = {
            "name": "web link scraper",
            "baseSelector": "//span[@class='V9tjod']",
            "fields": [
                {"name": "link", "selector": ".//a", "type": "attribute", "attribute": "href"}
            ]
        }
        self.final_results = []

    def return_base_url(self, keyword, index):
        return f"https://www.google.com/search?q={keyword}&start={index}"

    async def scrape_links(self, url:str):
        async with AsyncWebCrawler() as crawler:
            try:
                results = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        extraction_strategy=JsonXPathExtractionStrategy(self.schema)
                    )
                )
                data = json.loads(results.extracted_content)
                self.final_results.extend(data)
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
    
    def run_scraper(self, url):
        asyncio.run(self.scrape_links(url))
    
    def handle_threading(self, keyword):
        urls = [self.return_base_url(keyword=keyword, index=i) for i in range(0, 101, 10)]
        threads = []
        for url in urls:
            thread = Thread(target=self.run_scraper, args=(url,))
            threads.append(thread)
            thread.start()
            time.sleep(random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]))
        for thread in threads:
            thread.join()





