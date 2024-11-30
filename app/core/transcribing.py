import assemblyai as aai
import time
from loguru import logger
import os

from ..utils.convert_seconds import convert_seconds


def transcribing_aai(file_path: str) -> str:

    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API")
        logger.info("Обработка ASSEMBLY_AI_API прошла успешно")

    except Exception as err:
        logger.error(f"Ошибка при обработке ASSEMBLY_AI_API: {err}")

    transcriber = aai.Transcriber()
    audio_url = (file_path)
    config = aai.TranscriptionConfig(language_code="ru")

    try:
        logger.info("Начало транскрибации")

        start_time = time.perf_counter()
        transcript = transcriber.transcribe(audio_url, config)
        end_time = time.perf_counter()

        completion_time = end_time - start_time

        logger.info("Конец транскрибации")
        logger.info(f"Время выполения транскрибации: {convert_seconds(completion_time)}")

        return transcript.text
        
    except Exception as err:
        logger.error(f"Ошибка при транскрибации: {err}")
