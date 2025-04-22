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
def navigate_and_fetch(start_url: str, steps: list[dict]) -> str:
    """
    Multi‑step, human‑like navigation:
    steps = [
        {"action":"click_text",    "text":"Tender Announcement Information"},
        {"action":"click_selector","selector":"button[type='submit']"},
        {"action":"click_text",    "text":"JR Nara Station South Specific Land Rezoning Project Civil Engineering Technology Subcontracted"},
    ]
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page    = browser.new_page()
            page.goto(start_url, wait_until="networkidle")

            for step in steps:
                act = step["action"]
                if act == "click_text":
                    page.click(f"text={step['text']}")
                elif act == "click_selector":
                    page.click(step["selector"])
                elif act == "goto":
                    page.goto(step["url"], wait_until="networkidle")
                else:
                    # you can extend: 'fill', 'scroll', etc.
                    raise ValueError(f"Unknown action: {act}")
                page.wait_for_load_state("networkidle")

            html = page.content()
            browser.close()
            return html

    except Exception as e:
        raise RuntimeError(f"Navigation error: {e}")