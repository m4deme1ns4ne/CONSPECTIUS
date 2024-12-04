import assemblyai as aai
import time
from loguru import logger
import os

from ..utils.convert_seconds import convert_seconds


def transcribing_aai(file_path: str, language: str) -> str:
    """
    Эта функция принимает в качестве аргумента путь к аудиофайлу и
    транскрибирует его, используя API AssemblyAI.

    Args:
        file_path (str): Путь к транскрибируемому аудиофайлу.

    Returns:
        str: Транскрибированный текст.
    """
    # Обработка ключа API AssemblyAI
    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API")
        logger.info("Обработка ASSEMBLY_AI_API прошла успешно")

    except Exception as err:
        logger.error(f"Ошибка при обработке ASSEMBLY_AI_API: {err}") 

    # Создание экземпляра класса Transcriber и определение конфигурации транскрибации
    transcriber = aai.Transcriber()
    audio_url = (file_path)

    config = aai.TranscriptionConfig(punctuate=False, 
                                     format_text=False,
                                     language_code=language if language != "cancel" else None,
                                     language_detection=True if language == "cancel" else False)

    # Запуск транскрибации
    try:
        logger.info("Начало транскрибации")

        start_time = time.perf_counter()
        transcript = transcriber.transcribe(audio_url, config)
        end_time = time.perf_counter()

        completion_time = end_time - start_time

        logger.info("Конец транскрибации")
        logger.info(f"Время выполения транскрибации: {convert_seconds(completion_time)}")

        print(transcript.text)
        print()
        print(f"Длина текста: {len(transcript.text)}")
        return transcript.text
        
    except Exception as err:
        logger.error(f"Ошибка при транскрибации: {err}")
