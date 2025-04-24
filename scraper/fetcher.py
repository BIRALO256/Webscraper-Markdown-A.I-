# scraper/fetcher.py

import requests
from playwright.sync_api import sync_playwright
import time
import asyncio
from playwright.async_api import async_playwright

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
# scraper/fetcher.py (or wherever you keep it)

async def navigate_and_fetch(start_url: str, steps: list[dict]) -> str:
    """
    Your existing async multi-step navigator.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page    = await browser.new_page()
        await page.goto(start_url, wait_until="networkidle")

        for step in steps:
            act = step["action"]
            if act == "goto":
                await page.goto(step["url"], wait_until="networkidle")
            elif act == "click_text":
                await page.click(f"text={step['text']}", timeout=5000)
            elif act == "click_selector":
                await page.click(step["selector"], timeout=5000)
            elif act == "click_js":
                await page.evaluate(step["js"])
            elif act == "fill":
                await page.fill(step["selector"], step["value"])
            elif act == "wait":
                if "selector" in step:
                    await page.wait_for_selector(
                        step["selector"], timeout=step.get("timeout", 5000)
                    )
                else:
                    await asyncio.sleep(step.get("timeout", 1))
            else:
                raise ValueError(f"Unknown action: {act}")

            await page.wait_for_load_state("networkidle")

        html = await page.content()
        await browser.close()
        return html


def navigate_and_fetch_sync(start_url: str, steps: list[dict]) -> str:
    """
    Sync wrapper to run the async navigator under a Windows-compatible
    SelectorEventLoop in its own thread, so Playwright can spawn Chromium.
    """
    # 1) Force this thread to use SelectorEventLoopPolicy (supports subprocesses)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 2) Create a fresh event loop just for this call
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(
            navigate_and_fetch(start_url, steps)
        )
    finally:
        loop.close()