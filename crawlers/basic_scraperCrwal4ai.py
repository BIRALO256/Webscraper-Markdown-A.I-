import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    # Single JS command
    config = CrawlerRunConfig(
        js_code="window.scrollTo(0, document.body.scrollHeight);"
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com",  # Example site
            config=config
        )
        print("Crawled length:", len(result.cleaned_html))

    # Multiple commands
    js_commands = [
        "window.scrollTo(0, document.body.scrollHeight);",
        # 'More' link on Hacker News
        "document.querySelector('a.morelink')?.click();",  
    ]
    config = CrawlerRunConfig(js_code=js_commands)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com",  # Another pass
            config=config
        )
        print("After scroll+click, length:", len(result.cleaned_html))

if __name__ == "__main__":
    asyncio.run(main())
