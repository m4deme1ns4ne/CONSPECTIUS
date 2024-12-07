from loguru import logger
from openai import AsyncOpenAI
import httpx
import os

from app.core.promts_for_gpt import min_promt
from app.core.promts_for_gpt import middle_promt 
from app.core.promts_for_gpt import max_promt
from app.utils.count_tokens import count_tokens
from app.utils.split_text import TextSplitter


class GPTResponse:
    def __init__(self) -> None:
        self.api_key: str = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY не найден в переменных окружения.")
        
        self.proxies: str = os.getenv("PROXY", "")

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
                        model_gpt: str,
                        promt: str) -> str:
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
                    {"role": "system", "content": str(promt)},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content

        except Exception as err:
            logger.error(f"Ошибка при обработке запроса: {err}")
            raise Exception("Произошла ошибка при обработке запроса.")

    @logger.catch
    async def processing_transcribing(self, text: str, lenght_conspect: str) -> str:
        model_gpt = "gpt-4o-mini"

        ansver = ""

        if lenght_conspect == "low":
            res = await self.gpt_answer(
                                text=text,
                                model_gpt=model_gpt,
                                promt=min_promt.whole_part)
            ansver = res
            logger.info("Создан короткий конспект")

        elif lenght_conspect == "medium":
            splitter = TextSplitter(text)
            parts = splitter.split()
            for i, chunk in enumerate(parts):
                if i == 0:
                    res = await self.gpt_answer(
                                        text=chunk,
                                        model_gpt=model_gpt,
                                        promt=middle_promt.first_part)
                    ansver += f"{res}\n"
                else:
                    res = await self.gpt_answer(
                                        text=chunk,
                                        model_gpt=model_gpt,
                                        promt=middle_promt.second_part)
                    ansver += f"{res}\n"
            logger.info("Создан подробный конспект")

        elif lenght_conspect == "high":
            splitter = TextSplitter(text)
            parts = splitter.split()
            for i, chunk in enumerate(parts):
                if i == 0:
                    res = await self.gpt_answer(
                                        text=chunk,
                                        model_gpt=model_gpt,
                                        promt=max_promt.beginning_text)
                    ansver += f"{res}\n"
                elif i == 1:
                    res = await self.gpt_answer(
                                        text=chunk,
                                        model_gpt=model_gpt,
                                        promt=max_promt.middle_of_the_text)
                    ansver += f"{res}\n"
                else:
                    res = await self.gpt_answer(
                                        text=chunk,
                                        model_gpt=model_gpt,
                                        promt=max_promt.end_of_text)
                    ansver += f"{res}\n"
            logger.info("Создан очень подробный конспект")

        # Подсчет входных токенов 
        token_count_input = count_tokens(ansver, model=model_gpt)
        # Подсчёт выходных токенов
        token_count_output = count_tokens(text, model=model_gpt)

        logger.info(f"Конспект получен")
        logger.info(f"Количество входных токенов : {token_count_input}")
        logger.info(f"Количество выходных токенов: {token_count_output}")

        return ansver
