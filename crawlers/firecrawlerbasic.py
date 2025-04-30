# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key='fc-a36e8f5c73044677beb3648c469a49d0')

response = app.scrape_url(url='https://nara.efftis.jp/PPI/Public/PPUBC00100?kikanno=0201',
                        
                        formats=['markdown'],
agent={
    'model': 'FIRE-1',
    'prompt': 'Navigate through site and click this "入札公告情報" on the first page and then this selector "#PPUBC00400__search" on the second page and finally this text "ＪＲ奈良駅南特定土地区画整理事業土木技術補助業務委託" on the third page. and return the data as a markdown from the pop up page that appears.',
}
                        
                        )

print(response)