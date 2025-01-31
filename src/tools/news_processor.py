from bs4 import BeautifulSoup
import requests
from typing import Optional
import re


class ScrapeWebsiteTool:
    name: str = "itmo_news_scraper"
    description: str = "Поиск релевантной информации на сайте itmo.news по заданному запросу."

    @staticmethod
    def clean_from_html(string):
        return re.sub(r'\<[^>]*\>', '', string)

    def get_recent_news(self, query: str) -> Optional[str]:
        search_url = f"https://news.itmo.ru/ru/search/?search={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            return f"Ошибка запроса: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select(".weeklyevents")[0].select(".weeklyevent")
        if not articles:
            return "Ничего не найдено."

        results = []
        for article in articles:
            title = self.clean_from_html(str(article.a.text))
            summary = self.clean_from_html(str(article.p))
            link = "https://news.itmo.ru" + article.a["href"]
            results.append((title, summary, link))

        return results
