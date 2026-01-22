# tools/tab_manager.py
from playwright.sync_api import sync_playwright

class TabManager:
    def __init__(self):
        self.cdp_url = "http://127.0.0.1:9222"

    def get_upwork_tabs(self):
        """Finds all open Upwork tabs in the connected Chrome instance."""
        with sync_playwright() as p:
            try:
                # Connect to the browser window
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                context = browser.contexts[0]
                tabs = []
                
                print(f"DEBUG: Scanning {len(context.pages)} open tabs...")
                
                for page in context.pages:
                    url = page.url.lower()
                    # Check for ANY Upwork freelancer profile format
                    if "upwork.com" in url and "/freelancers/" in url:
                        print(f"✅ Found Profile: {url}")
                        tabs.append({
                            "title": page.title(),
                            "url": page.url,
                            "is_competitor": True
                        })
                
                browser.close()
                return tabs
            except Exception as e:
                print(f"❌ Tab Hunter Error: {e}")
                return []