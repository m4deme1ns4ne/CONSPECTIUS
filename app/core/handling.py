import os
from dataclasses import asdict, dataclass

import httpx
from loguru import logger
from openai import AsyncOpenAI

from app.errors.empty_text import EmptyTextError
from app.templates.promts_for_gpt import max_promt, min_promt
from app.utils.count_tokens import count_tokens
from app.utils.part_of_text import get_part_text


@dataclass
class Conspect:
    title: str
    key_terms_and_concepts: str
    chronological_lecture_outline: str
    mini_test: str


class GPTConfig:
    """Класс с данными конфигурации GPT."""

    def __init__(self) -> None:
        self._gpt_api_key: str = os.getenv("OPENAI_API_KEY", "")
        if not self._gpt_api_key:
            raise ValueError(
                "OPENAI_API_KEY не найден в файле .env или переменных окружения."
            )
        # Прокси опционально
        self._proxies: str = os.getenv("PROXY", "")

    @property
    def gpt_api_key(self):
        return self._gpt_api_key

    @property
    def proxies(self):
        return self._proxies


class GPTClient:
    """Класс для создания клиента GPT."""

    def __init__(self, config: GPTConfig) -> None:
        self._config: GPTConfig = config

    @property
    def config(self):
        return self._config

    async def create_openai_client(self):
        """
        Создание клиента OpenAI.
        """
        return AsyncOpenAI(
            api_key=self.config._gpt_api_key,
            http_client=httpx.AsyncClient(
                proxies=self.config._proxies,
                transport=httpx.HTTPTransport(
                    local_address=self.config._proxies
                ),
            ),
        )


class GPTResponse:
    """Класс для получения ответа от GPT."""

    def __init__(self, gpt_client: GPTClient) -> None:
        self._gpt_client: GPTClient = gpt_client

    @property
    def gpt_client(self):
        return self._gpt_client

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
        client: GPTClient = await self.gpt_client.create_openai_client()

        # Отправляем запрос в GPT
        response = await client.chat.completions.create(
            model=model_gpt,
            messages=[
                {"role": "system", "content": str(promt)},
                {"role": "user", "content": text},
            ],
        )

        answer_gpt = response.choices[0].message.content

        if answer_gpt is None:
            logger.info("Ответ gpt пустой")
            raise EmptyTextError()

        return answer_gpt


class ConspectConstructor:
    def __init__(self, gpt_response: GPTResponse):
        self.gpt_response: GPTResponse = gpt_response

    async def short_conspect(self, text: str, model_gpt: str) -> str:
        conspect = await self.gpt_answer(text, model_gpt, min_promt.whole_part)
        logger.info("Создан короткий конспект")
        return conspect

    async def detailed_conspect(self, text: str, model_gpt: str) -> str:
        # Получаем части и добавляем их в конспект

        # Название (только 30 процентов от текста)
        title: str = await self.gpt_response.gpt_answer(
            get_part_text(text, percent=15), model_gpt, max_promt.title
        )
        # Термины и понятия
        key_terms_and_concepts: dict = await self.gpt_response.gpt_answer(
            text, model_gpt, max_promt.key_terms_and_concepts
        )
        # Хронологический конспект лекции
        chronological_lecture_outline: str = (
            await self.gpt_response.gpt_answer(
                text,
                model_gpt,
                max_promt.chronological_lecture_outline,
            )
        )
        # Небольшой тест лекции
        mini_test: str = await self.gpt_response.gpt_answer(
            f"{key_terms_and_concepts}/n/n{chronological_lecture_outline}",
            model_gpt,
            max_promt.mini_test,
        )
        # Получаем итоговый текст
        conspect: dataclass = Conspect(
            title=title,
            key_terms_and_concepts=key_terms_and_concepts,
            chronological_lecture_outline=chronological_lecture_outline,
            mini_test=mini_test,
        )

        logger.info("Создан подробный конспект")
        return conspect

    async def processing_conspect(
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
            conspect = await self.short_conspect(text, model_gpt)

        # Подробный конспект
        else:
            conspect = await self.detailed_conspect(text, model_gpt)

        try:
            # Подсчет входных токенов
            token_count_input = count_tokens(text, model=model_gpt)
            # Подсчёт выходных токенов
            token_count_output = sum(
                [
                    count_tokens(value, model=model_gpt)
                    for value in asdict(conspect).values()
                ]
            )

            logger.debug(
                f"Количество входных токенов: {token_count_input}, Количество выходных токенов: {token_count_output}"
            )
        except Exception as err:
            logger.info(f"Произошла ошибка при отображении токенов: {err}")

        return conspect
