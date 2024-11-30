from loguru import logger
from openai import AsyncOpenAI
import httpx
import os

from .promt_for_gpt import role_system
from ..utils.split_text import split_text
from ..utils.count_tokens import count_tokens

class GPTResponse:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.proxies = os.getenv("PROXY")
        self.local_address = "0.0.0.0"

    async def get_openai_client(self):
        """
        Создание клиента OpenAI.
        """
        return AsyncOpenAI(
            api_key=self.api_key,
            http_client=httpx.AsyncClient(
                proxies=self.proxies,
                transport=httpx.HTTPTransport(local_address=self.proxies)
            )
        )

    @logger.catch
    async def gpt_answer(self,
                        text: str,
                        model_gpt: str) -> str:
        """
        Отправляет вопрос модели GPT и обрабатывает ответ.

        :param question (str): Строка с вопросом или запросом пользователя.
        :param model_gpt (str): Строка, обозначающая используемую модель GPT.
        :param telegram_id (int): Целочисленный идентификатор пользователя в Telegram.

        :return: Ответ от модели GPT в виде строки.
        """
        try:
            # Создаем клиент OpenAI
            client = await self.get_openai_client()

            # Отправляем запрос в GPT
            response = await client.chat.completions.create(
                model=model_gpt,
                messages=[
                    {"role": "system", "content": str(role_system)},
                    {"role": "user", "content": f"{text}"}
                ]
            )
            return response.choices[0].message.content

        except Exception as err:
            logger.error(f"Ошибка при обработке запроса: {err}")
            raise Exception("Произошла ошибка при обработке запроса.")

    @logger.catch
    async def processing_transcribing(self, text: str) -> str:
        split_texts = split_text(text)
        model_gpt = "gpt-4o-mini"

        ansver = ""
        for chunk in split_texts:
            res = await self.gpt_answer(text=chunk,
                                model_gpt=model_gpt)
            ansver += f"{res}\n"

        model_name = "gpt-4o-mini"  # Укажите модель, которую вы используете
        token_count = count_tokens(text, model=model_name)

        logger.info(f"Конспект получен")
        logger.info(f"Количество токенов для запроса: {token_count}")

        return ansver
