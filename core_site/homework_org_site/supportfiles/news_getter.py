import feedparser
from bs4 import BeautifulSoup as bf

def news_getter() -> tuple[list, list, list]:
    feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
    titles = []
    links = []
    contents = []
    for entry in feed.entries[:5]:
        content = entry.content[0].value
        soup = bf(content, 'html.parser')
        titles.append(entry.title)
        links.append(entry.link)
        contents.append(soup.get_text(strip=True))
    return titles, links, contents
