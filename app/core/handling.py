import os
import time
from dataclasses import asdict, dataclass

from loguru import logger
from openai import AsyncOpenAI

from app.errors.empty_text import EmptyTextError
from app.templates.promts_for_gpt import max_promt, min_promt
from app.utils import count_tokens, get_part_text, remove_markdown


@dataclass
class Conspect:
    title: str = None
    key_terms_and_concepts: str = None
    chronological_lecture_outline: str = None
    mini_test: str = None
    summary: str = None


class GPTConfig:
    """Класс с данными конфигурации GPT."""

    def __init__(self) -> None:
        self._gpt_api_key: str = os.getenv("OPENAI_API_KEY", "")
        if not self._gpt_api_key:
            raise ValueError(
                "OPENAI_API_KEY не найден в файле .env или переменных окружения."
            )

    @property
    def gpt_api_key(self):
        return self._gpt_api_key


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
            base_url="https://openrouter.ai/api/v1",
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
            extra_body={},
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
        # Саммари текста
        summary: dict = await self.gpt_response.gpt_answer(
            text, model_gpt, min_promt.summary
        )
        if summary is not None:
            logger.debug(
                f"Создано саммари для короткого конспекта: type({type(summary)})"
            )
        else:
            raise EmptyTextError("Саммари для короткого конспекта пустое")

        # Название, создается на основе summary
        title: str = await self.gpt_response.gpt_answer(
            summary, model_gpt, min_promt.title
        )
        if title is not None:
            logger.debug(
                f"Создано название для короткого конспекта: type({type(title)})"
            )
        else:
            raise EmptyTextError("Название для короткого конспекта пустое")

        conspect: dataclass = Conspect(
            title=remove_markdown(title), summary=remove_markdown(summary)
        )
        logger.info("Создан короткий конспект")

        return conspect

    async def detailed_conspect(self, text: str, model_gpt: str) -> str:
        # Получаем части и добавляем их в конспект

        # Название (только 30 процентов от текста)
        title: str = await self.gpt_response.gpt_answer(
            get_part_text(text, percent=30), model_gpt, max_promt.title
        )
        if title is not None:
            logger.debug(
                f"Создано название для подробного конспекта: type({type(title)})"
            )
        else:
            raise EmptyTextError("Название для подробного конспекта пустое")

        # Термины и понятия
        key_terms_and_concepts: dict = await self.gpt_response.gpt_answer(
            text, model_gpt, max_promt.key_terms_and_concepts
        )
        if key_terms_and_concepts is not None:
            logger.debug(
                f"Созданы термины и понятия для подробного конспекта: type({type(key_terms_and_concepts)})"
            )
        else:
            raise EmptyTextError(
                "Термины и понятия для подробного конспекта пустые"
            )

        # Хронологический конспект лекции
        chronological_lecture_outline: str = (
            await self.gpt_response.gpt_answer(
                text,
                model_gpt,
                max_promt.chronological_lecture_outline,
            )
        )
        if chronological_lecture_outline is not None:
            logger.debug(
                f"Создано хронологический конспект лекции для подробного конспекта: type({type(chronological_lecture_outline)})"
            )
        else:
            raise EmptyTextError(
                "Хронологический конспект лекции для подробного конспекта пустой"
            )

        # Небольшой тест лекции
        mini_test: str = await self.gpt_response.gpt_answer(
            f"{key_terms_and_concepts}/n/n{chronological_lecture_outline}",
            model_gpt,
            max_promt.mini_test,
        )
        if mini_test is not None:
            logger.debug(
                f"Создано небольшой тест лекции для подробного конспекта: type({type(mini_test)})"
            )
        else:
            raise EmptyTextError(
                "Небольшой тест лекции для подробного конспекта пустой"
            )

        # Получаем итоговый текст
        conspect: dataclass = Conspect(
            title=remove_markdown(title),
            key_terms_and_concepts=remove_markdown(key_terms_and_concepts),
            chronological_lecture_outline=remove_markdown(
                chronological_lecture_outline
            ),
            mini_test=remove_markdown(mini_test),
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
        model_gpt: str = "deepseek/deepseek-r1:free"

        logger.debug("Начало обработки текста")

        start_time: time = time.perf_counter()

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
                    if value is not None
                ]
            )

            logger.info(
                f"Количество входных токенов: {token_count_input}, Количество выходных токенов: {token_count_output}"
            )
        except Exception as err:
            logger.error(f"Произошла ошибка при отображении токенов: {err}")

        end_time: time = time.perf_counter()

        completion_time: int = end_time - start_time

        logger.debug(f"Время обработки транскрибации: {completion_time}")

        return conspect
