import asyncio
import os
import time

import assemblyai as aai
from loguru import logger

from app.errors.empty_text import EmptyTextError
from app.utils.convert_seconds import convert_seconds
from app.utils.upload_file import upload_file


class AssemblyAIConfig:
    """Класс с данными конфигурации AssemblyAI."""

    def __init__(self) -> None:
        self._assemblyai_api_key: str = os.getenv("ASSEMBLY_AI_API", "")
        if not self._assemblyai_api_key:
            raise ValueError(
                "ASSEMBLY_AI_API не найден в файле .env или переменных окружения."
            )
        aai.settings.api_key = self._assemblyai_api_key

    @property
    def assemblyai_api_key(self):
        return self._assemblyai_api_key


class AudioToText:
    """Класс для получения ответа от AssemblyAI."""

    def __init__(self, config: AssemblyAIConfig):
        self.config: AssemblyAIConfig = config
        self.transcriber: aai.Transcriber = aai.Transcriber()

    async def transcribing(self, file_path: str, language: str) -> str:
        """
        Транскрибирует аудиофайл с использованием API AssemblyAI.

        Args:
            file_path (str): Путь к аудиофайлу для транскрибации.
            language (str): Код языка для транскрибации или "cancel" для автоматического определения языка.

        Returns:
            str: Транскрибированный текст.
        """
        # Общие параметры конфигурации транскрибации
        common_config: dict[str:bool, str:bool] = {
            # Пунктуация
            "punctuate": True,
            # Форматирование текста
            "format_text": True,
        }

        # Настройка конфигурации транскрибации с учетом языка
        if language == "cancel":
            config = aai.TranscriptionConfig(
                **common_config, language_detection=True
            )
        else:
            config = aai.TranscriptionConfig(
                **common_config, language_code=language
            )

        # Загрузка файла
        logger.debug("Загрузка файла для транскрибации.")
        audio_url: str = await upload_file(file_path)
        logger.debug(f"Файл успешно загружен. URL: {audio_url}")
        logger.debug("Начало транскрибации")

        start_time: time = time.perf_counter()

        # Инициация транскрипции и получение Future
        job_future = self.transcriber.transcribe_async(audio_url, config)

        # Оборачивание concurrent.futures.Future в asyncio.Future
        job: asyncio.Future = await asyncio.wrap_future(job_future)

        end_time: time = time.perf_counter()
        completion_time: int = end_time - start_time

        if job.status == "completed":
            logger.debug(
                f"Транскрибация завершена успешно. Время выполнения: {convert_seconds(completion_time)}"
            )
            return job.text
        else:
            logger.error(
                f"Транскрибация завершилась со статусом: {job.status}"
            )
            raise EmptyTextError("Пустая транскрибация")
