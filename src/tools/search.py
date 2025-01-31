import requests
from config import Config


class SearchAgent:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    async def search(self, query):
        params = {
            "key": Config.SEARCH_API_KEY,
            "cx": Config.SEARCH_ENGINE_ID,
            "q": query + " site:itmo.ru",
            "num": 3
        }
        try:
            response = requests.get(self.base_url, params=params)
            results = response.json().get("items", [])[:3]

            context = "Результаты поиска:\n\n"
            for i, item in enumerate(results, 1):
                context += f"{i}. {item.get('title', 'Без названия')}\n"
                context += f"Ссылка: {item.get('link', '')}\n"
                context += f"Описание: {item.get('snippet', 'Нет описания')}\n\n"

            return context

        except Exception as e:
            return f"Ошибка при поиске: {str(e)}"
