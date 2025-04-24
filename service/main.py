# service/main.py

import sys, asyncio
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from pydantic import BaseModel
from typing import List, Dict

# On Windows, ensure compatibility for any other async operations
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from scraper.fetcher      import fetch_page, navigate_and_fetch
from processor.markdownifier import html_to_markdown
from processor.llm_extractor import extract_fields

app = FastAPI()

FIELDS = [
    "bidding_method",
    "registration_date",
    "bid_title",
    "winning_bidders",
    "winning_bid_amount",
    "announcement_date",
    "result_date",
    "prefecture",
    "agency"
]


class NavRequest(BaseModel):
    url: str
    steps: List[Dict[str, str]]



@app.get("/scrape")
async def scrape_and_extract(url: str):
    # 1) Fetch HTML via requests in a worker thread
    try:
        html = await run_in_threadpool(fetch_page, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching page: {e}")

    # 2) Convert HTML → Markdown
    markdown = html_to_markdown(html)
    
    print("\n📝 Extracted Markdown:\n", markdown[:2000])  # First 2000 chars.


    # 3) Send Markdown to LLM for field extraction
    try:
        data = extract_fields(markdown, FIELDS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting fields: {e}")

    return data

@app.post("/scrape/nav")
async def scrape_with_navigation(req: NavRequest):
        try:
            html = await navigate_and_fetch(req.url, req.steps)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Navigation error: {e}")

        md = html_to_markdown(html)

        try:
            return extract_fields(md, FIELDS)
        except Exception as e:
            raise HTTPException(500, f"Error extracting fields: {e}")