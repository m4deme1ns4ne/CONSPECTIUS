import os

import httpx
from loguru import logger
from openai import AsyncOpenAI

from app.core.promts_for_gpt import max_promt, middle_promt, min_promt
from app.utils.count_tokens import count_tokens
from app.utils.split_text import TextSplitter


class GPTResponse:
    def __init__(self) -> None:
        self.api_key: str = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY не найден в переменных окружения."
            )

        self.proxies: str = os.getenv("PROXY", "")

    async def get_openai_client(self):
        """
        Создание клиента OpenAI.
        """
        return AsyncOpenAI(
            api_key=self.api_key,
            http_client=httpx.AsyncClient(
                proxies=self.proxies,
                transport=httpx.HTTPTransport(local_address=self.proxies),
            ),
        )

    @logger.catch
    async def gpt_answer(self, text: str, model_gpt: str, promt: str) -> str:
        # Создаем клиент OpenAI
        client = await self.get_openai_client()

        # Отправляем запрос в GPT
        response = await client.chat.completions.create(
            model=model_gpt,
            messages=[
                {"role": "system", "content": str(promt)},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content

    async def processing_transcribing(
        self, text: str, lenght_conspect: str
    ) -> str:
        """Обрабатывает создание конспекта на основе заданной длины."""
        model_gpt = "gpt-4o-mini"

        # Инициализация пустой строки для конспекта
        ansver = ""

        # Короткий конспект
        if lenght_conspect == "low":
            ansver = await self.gpt_answer(
                text, model_gpt, min_promt.whole_part
            )
            logger.info("Создан короткий конспект")

        # Средний конспект
        elif lenght_conspect == "medium":
            splitter = TextSplitter(text)
            parts = splitter.split()
            first_part = await self.gpt_answer(
                text=parts[0],
                model_gpt=model_gpt,
                promt=middle_promt.first_part,
            )
            second_part = await self.gpt_answer(
                text=parts[1],
                model_gpt=model_gpt,
                promt=middle_promt.second_part,
            )

            # Получаем итоговый текст
            ansver = f"{first_part}\n{second_part}"

            logger.info("Создан подробный конспект")

        # Подробный конспект
        else:
            splitter = TextSplitter(text)
            parts = splitter.split()

            # Получаем части и добавляем их в конспект
            first_part = await self.gpt_answer(
                parts[0], model_gpt, max_promt.beginning_text
            )
            second_part = await self.gpt_answer(
                parts[1], model_gpt, max_promt.middle_of_the_text
            )
            third_part = await self.gpt_answer(
                parts[2], model_gpt, max_promt.end_of_text
            )

            # Получаем итоговый текст
            ansver = f"{first_part}\n{second_part}\n{third_part}"

            logger.info("Создан очень подробный конспект")

        # Подсчет входных токенов
        token_count_input = count_tokens(ansver, model=model_gpt)
        # Подсчёт выходных токенов
        token_count_output = count_tokens(text, model=model_gpt)

        logger.debug(
            f"Количество входных токенов: {token_count_input}, Количество выходных токенов: {token_count_output}"
        )

        return ansver
