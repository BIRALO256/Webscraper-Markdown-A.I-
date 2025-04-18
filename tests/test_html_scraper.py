from scraper.html_scraper import scrape_list_page

def test_scrape_list_page():
    links = scrape_list_page()
    assert isinstance(links, list)