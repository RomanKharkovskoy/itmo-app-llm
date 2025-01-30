from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import asyncio

from config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)


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
