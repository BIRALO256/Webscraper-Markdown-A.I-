from scraper.playwright_scraper import scrape_page

def test_scrape_page_returns_html():
    html = scrape_page('https://example.com')
    assert '<html' in html.lower()