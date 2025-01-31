from __future__ import annotations
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.agents.agent import BaseSingleActionAgent
from langchain_community.llms.yandex import YandexGPT
from src.tools.search_tools import SearchTools
from src.tools.news_processor import ScrapeWebsiteTool
from config import Config
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import json
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class Answer(BaseModel):
    answer: str = Field(description="answer")
    reasoning: str = Field(description="reasoning")
    sources: list[str] = Field(description="sources")


class WebSearchInput(BaseModel):
    query: str


class ITMOAssistant:
    def __init__(self):
        self.llm = YandexGPT(
            api_key=Config.YANDEX_API_KEY,
            temperature=0.3,
            folder_id="b1gpne5muq976fbjjbke"
        )
        self.search_tools = SearchTools()
        self.news_processor = ScrapeWebsiteTool()

        self.agent = self._create_agent()

    def _create_agent(self):
        self.tools = [
            StructuredTool(
                name="Web Search",
                func=self.search_tools.web_search,
                description="Для поиска информации об Университете ИТМО",
                args_schema=WebSearchInput
            ),
            Tool(
                name="ITMO News",
                func=self.news_processor.get_recent_news,
                description="Для получения последних новостей ИТМО"
            )
        ]
        return initialize_agent(
            tools=self.tools,
            llm=self.llm
        )

    def _generate_parser(self):
        return JsonOutputParser(pydantic_object=Answer)

    def generate_answer(self, question):
        prompt = self._create_prompt().format(question=question)
        parser = self._generate_parser()

        try:
            response = self.agent.invoke({"input": prompt})
            parsed_answer = parser.parse(response["output"])
        except ValueError as e:
            print(f"Ошибка парсинга: {e}")
            raw_output = str(e).split("This is the error:")[-1].strip()
            parsed_answer = self._attempt_manual_parsing(raw_output)

        return parsed_answer

    def _attempt_manual_parsing(self, raw_output):
        """
        Попытка вручную распарсить невалидный JSON-ответ.
        """
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            answer, reasoning, sources = None, "", []
            for line in raw_output.split("\n"):
                if line.startswith("answer:"):
                    try:
                        answer = int(line.split("answer:")[1].strip())
                    except ValueError:
                        answer = None  # Оставляем None, если не число
                elif line.startswith("reasoning:"):
                    reasoning = line.split("reasoning:")[1].strip()
                elif line.startswith("sources:"):
                    sources = line.split("sources:")[1].strip()

            return {"answer": answer, "reasoning": reasoning, "sources": sources}

    def _create_prompt(self):
        return PromptTemplate(
            template="""
            Ответь на вопрос пользователя, используя информацию из предоставленных данных.
            Если вопрос содержит варианты ответов, то необходимо выбрать один из них, который будет выведен в поле answer
            Вопрос: {question}
            Ответ формулируй на русском языке.
            СТРОГО используй следующую структуру!
            {{
            "answer": числовое значение, содержащее правильный ответ на вопрос (если вопрос подразумевает выбор из вариантов). Если вопрос не предполагает выбор из вариантов, значение должно быть null.
            "reasoning": текстовое поле, содержащее объяснение или дополнительную информацию по запросу.
            "sources": ссылки на источники, где была взята данная информация, в формате first_link.ru, second_link.ru (Если источники не требуются, значение должно быть пустым списком [])
            }}
            Пример:
            {{
            Ввод: Сколько стоят жевачки по рублю?\n1. 4 рубля\n2. 2 рубля\n3. 3 рубля\n4. 1 рубль\n5. 5 рублей
            Вывод:
            answer: 4,
            reasoning: "Согласно данному ресурсу жевачки по рублю стоят 1 рубль",
            sources: [bublegum_prices.ru]
            }}
            """,
            input_variables=["question"]
        )


if __name__ == "__main__":
    assistant = ITMOAssistant()
    parser = JsonOutputParser(pydantic_object=Answer)
    question = "В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015"
    answer = assistant.generate_answer(question)
    with open("/home/roman/University/Diploma/itmo-app-llm/answer.json", "w", encoding="utf-8") as f:
        json.dump(answer, f, ensure_ascii=False, indent=2)
