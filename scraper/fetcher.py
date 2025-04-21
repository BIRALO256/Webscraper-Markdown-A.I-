# scraper/fetcher.py

import requests
from playwright.sync_api import sync_playwright

def fetch_page(url: str, use_browser: bool = False) -> str:
    if use_browser:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle")
                html = page.content()
                browser.close()
                return html
        except Exception as e:
            raise RuntimeError(f"Playwright error: {e}")
    else:
        try:
            resp = requests.get(url, timeout=15, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            raise RuntimeError(f"Requests error: {e}")
