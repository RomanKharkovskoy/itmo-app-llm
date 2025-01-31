from __future__ import annotations
from langchain_community.llms.yandex import YandexGPT
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import Config
import asyncio

llm = YandexGPT(
    api_key=Config.YANDEX_API_KEY,
    folder_id=Config.YANDEX_FOLDER_ID
)


class ResponseAgent:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template(
            """Ответь на вопрос пользователя, используя информацию из предоставленных данных.
            
            Данные для ответа:
            {context}
            
            Вопрос: {question}
            Если в вопросе есть Варианты ответа, то отправь только цифру номер правильного ответа.
            Ответ формулируй на русском языке, будь краток и точен.
            Формат вывода ответа на вопрос:
            answer: ...
            reasoning: ...
            sources: ссылки на источники, где была взята данная информация, в формате first_link.ru, second_link.ru
            """
        )

        self.chain = self.prompt | llm | StrOutputParser()

    def _format_question_and_answers(self, input_string):
        question, *answers = input_string.split('\n')
        formatted_string = f"{question}\nВарианты ответа:\n" + \
            "\n".join(answers)

        return formatted_string

    async def generate_response(self, question, context):
        if "\n" in question:
            question = self._format_question_and_answers(question)
        return await self.chain.ainvoke({"question": question, "context": context})
