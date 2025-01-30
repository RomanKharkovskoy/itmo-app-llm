from bs4 import BeautifulSoup
import requests
import asyncio


class NewsAgent:
    def __init__(self):
        self.news_url = "https://news.itmo.ru/ru/search/?search="

    async def get_news(self):
        try:
            response = requests.get(self.news_url)
            soup = BeautifulSoup(response.text, "html.parser")

            news_items = []
            for article in soup.select(".media__content")[:3]:
                title = article.find("h3").text.strip()
                link = article.find("a")["href"]
                if not link.startswith("http"):
                    link = f"https://news.itmo.ru{link}"
                news_items.append({"title": title, "link": link})

            return news_items
        except Exception as e:
            return []


async def main():
    agent = NewsAgent()
    news = await agent.get_news()
    for item in news:
        print(f"Title: {item['title']}\nLink: {item['link']}\n")

if __name__ == "__main__":
    asyncio.run(main())
