# service/main.py
from fastapi import FastAPI
from scraper.playwright_scraper import fetch_page_html   # <-- change here
from processor.markdownifier import html_to_markdown
from processor.llm_extractor import extract_fields

app = FastAPI()
FIELDS = ["title", "price", "weight", "description", "category", "features"]

@app.get("/scrape")
def scrape_and_extract(url: str):
    html = fetch_page_html(url)                    # now gets full DOM
    markdown = html_to_markdown(html)              # convert to Markdown
    data = extract_fields(markdown, FIELDS)        # LLM pulls your fields
    return data
