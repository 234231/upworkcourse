import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("email")
PASSWORD = os.getenv("password")
LOGIN_URL = os.getenv("url")

async def run_lms_scraper():
    async with async_playwright() as p:
        # Use a persistent browser so we don't get flagged as a bot
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser_session",
            headless=False  # Set to True once you confirm it logs in correctly
        )
        page = await context.new_page()

        print(f"[*] Navigating to {LOGIN_URL}...")
        await page.goto(LOGIN_URL)

        # 1. Login Logic
        try:
            # Check if already logged in by looking for email field
            if await page.query_selector('input[type="email"]'):
                await page.fill('input[type="email"]', EMAIL)
                await page.fill('input[type="password"]', PASSWORD)
                await page.click('button[type="submit"]') # Or the specific login button
                await page.wait_for_load_state("networkidle")
                print("[+] Login Successful!")
        except Exception as e:
            print(f"[!] Login error or already logged in: {e}")

        # 2. Navigate to Courses
        # NOTE: You'll need to update this URL to the actual 'My Courses' page
        print("[*] Finding lectures...")
        # This is a generic selector. We may need to tweak this 
        # based on how your specific LMS lists videos.
        lectures = await page.locator("a[href*='/lectures/']").all()
        
        lecture_links = []
        for lec in lectures:
            link = await lec.get_attribute("href")
            title = await lec.inner_text()
            lecture_links.append({"title": title.strip(), "url": link})

        print(f"[+] Found {len(lecture_links)} lectures.")
        return lecture_links, page

if __name__ == "__main__":
    asyncio.run(run_lms_scraper())