# tools/scraper.py
from playwright.sync_api import sync_playwright

class UpworkScraper:
    def __init__(self):
        # Change localhost to 127.0.0.1 to avoid IPv6 issues
        self.cdp_url = "http://127.0.0.1:9222"
    def scrape_url(self, url: str):
        """Scrapes a single profile URL using the open Chrome session."""
        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                context = browser.contexts[0]
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Extracting headline and bio
                data = {
                    "url": url,
                    "headline": page.inner_text("h2.mt-10") if page.query_selector("h2.mt-10") else "N/A",
                    "bio": page.inner_text("span.break-word") if page.query_selector("span.break-word") else "N/A"
                }
                page.close()
                return data
            except Exception as e:
                return {"url": url, "error": str(e)}