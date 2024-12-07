import asyncio
import os
import time

import assemblyai as aai
from loguru import logger

from ..utils.convert_seconds import convert_seconds
from ..utils.upload_file import upload_file


async def transcribing_aai(file_path: str, language: str) -> str:
    """
    Эта функция принимает путь к аудиофайлу и транскрибирует его с использованием API AssemblyAI.

    Args:
        file_path (str): Путь к аудиофайлу для транскрибации.
        language (str): Код языка для транскрибации или "cancel" для автоматического определения языка.

    Returns:
        str: Транскрибированный текст.
    """
    # Обработка ключа API AssemblyAI
    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API")
        logger.info("Ключ API AssemblyAI обработан успешно.")
    except Exception as err:
        logger.error(f"Ошибка при обработке ASSEMBLY_AI_API: {err}")
        return ""

    # Инициализация Transcriber и настройка конфигурации транскрибации
    transcriber = aai.Transcriber()

    if language == "cancel":
        config = aai.TranscriptionConfig(
            punctuate=False, format_text=False, language_detection=True
        )
    else:
        config = aai.TranscriptionConfig(
            punctuate=True, format_text=True, language_code=language
        )

    # Начало транскрибации
    try:
        logger.info("Загрузка файла для транскрибации.")
        audio_url = await upload_file(file_path)
        logger.info("Файл успешно загружен. Начало транскрибации.")

        start_time = time.perf_counter()

        # Инициация транскрипции и получение Future
        job_future = transcriber.transcribe_async(audio_url, config)

        # Оборачивание concurrent.futures.Future в asyncio.Future
        job = await asyncio.wrap_future(job_future)

        end_time = time.perf_counter()

        completion_time = end_time - start_time

        if job.status == "completed":
            transcription_text = job.text
            logger.info("Транскрибация завершена успешно.")
            logger.info(
                f"Время выполнения транскрибации: {convert_seconds(completion_time)}"
            )
            return transcription_text
        else:
            logger.error(
                f"Транскрибация завершилась со статусом: {job.status}"
            )
            return ""

    except Exception as err:
        logger.error(f"Ошибка при транскрибации: {err}")
        raise Exception()
