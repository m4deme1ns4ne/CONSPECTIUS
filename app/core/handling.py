import os

import httpx
from loguru import logger
from openai import AsyncOpenAI

from app.errors.empty_text import EmptyTextError
from app.templates.promts_for_gpt import max_promt, middle_promt, min_promt
from app.utils.count_tokens import count_tokens
from app.utils.split_text import TextSplitter


class GPTResponse:
    def __init__(self) -> None:
        self.api_key: str = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY не найден в файле .env или переменных окружения."
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
        """Получения ответа от GPT

        Args:
            text (str): Текст запроса
            model_gpt (str): Модель gpt
            promt (str): Промт для запроса

        Returns:
            str: Результат ответа gpt
        """
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
        """Обрабатывает создание конспекта на основе заданной длины.

        Args:
            text (str): Транскрибация, которую нужно обработать
            lenght_conspect (str): Желаемая длина конспекта

        Returns:
            str: Конечный конспект
        """
        model_gpt: str = "gpt-4o-mini"

        # Короткий конспект
        if lenght_conspect == "low":
            conspect: str = await self.gpt_answer(
                text, model_gpt, min_promt.whole_part
            )
            logger.info("Создан короткий конспект")

        # Средний конспект
        elif lenght_conspect == "medium":
            splitter = TextSplitter(text)
            splitter_text: str = splitter.split(n_parts=2)
            first_part_conspect: str = await self.gpt_answer(
                text=splitter_text,
                model_gpt=model_gpt,
                promt=middle_promt.first_part,
            )
            second_part_conspect: str = await self.gpt_answer(
                text=splitter_text,
                model_gpt=model_gpt,
                promt=middle_promt.second_part,
            )

            # Получаем итоговый текст
            conspect: str = f"{first_part_conspect}\n{second_part_conspect}"

            logger.info("Создан подробный конспект")

        # Подробный конспект
        else:
            splitter = TextSplitter(text)
            splitter_text: str = splitter.split(n_parts=3)

            # Получаем части и добавляем их в конспект
            first_part_conspect: str = await self.gpt_answer(
                splitter_text, model_gpt, max_promt.beginning_text
            )
            second_part_conspect: str = await self.gpt_answer(
                splitter_text, model_gpt, max_promt.middle_of_the_text
            )
            third_part_conspect: str = await self.gpt_answer(
                splitter_text, model_gpt, max_promt.end_of_text
            )

            # Получаем итоговый текст
            conspect: str = (
                f"{first_part_conspect}\n{second_part_conspect}\n{third_part_conspect}"
            )

            logger.info("Создан очень подробный конспект")

        if not conspect:
            logger.error("Конспект пустой")
            raise EmptyTextError()

        # Подсчет входных токенов
        token_count_input = count_tokens(text, model=model_gpt)
        # Подсчёт выходных токенов
        token_count_output = count_tokens(conspect, model=model_gpt)

        logger.debug(
            f"Количество входных токенов: {token_count_input}, Количество выходных токенов: {token_count_output}"
        )

        return conspect
