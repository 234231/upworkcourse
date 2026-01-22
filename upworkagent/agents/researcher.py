# agents/researcher.py
import time
from tools.scraper import UpworkScraper
from tools.tab_manager import TabManager

class ResearcherNode:
    def __init__(self):
        self.scraper = UpworkScraper()
        self.tab_hunter = TabManager()

    def work(self, state: dict):
        print("Researcher Node is starting work...")
        urls = state.get("urls", [])
        
        # Give the connection a moment to breathe
        time.sleep(1) 
        
        if not urls:
            tabs = self.tab_hunter.get_upwork_tabs()
            if isinstance(tabs, list) and len(tabs) > 0:
                # Let's be less strict. If it's Upwork, let's try to scrape it!
                urls = [tab['url'] for tab in tabs if "upwork.com" in tab['url']]
        
        if not urls:
            print("⚠️ No Upwork URLs found in the debug browser.")
            # Instead of failing, let's ask the Analyst to wait for a paste
            return {"competitors": [], "next_node": "analyst"}

        scraped_results = []
        for url in urls:
            # Skip the 'json' and 'newtab' pages
            if "127.0.0.1" in url or "newtab" in url:
                continue
                
            print(f"Scraping: {url}")
            data = self.scraper.scrape_url(url)
            if data and "error" not in data:
                scraped_results.append(data)
            
        return {
            "competitors": scraped_results,
            "next_node": "analyst"
        }