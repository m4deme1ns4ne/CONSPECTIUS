import assemblyai as aai
import time
from loguru import logger
import os
from dotenv import load_dotenv
import sys


@logger.catch
def transcribing_aai() -> str:
    
    load_dotenv()

    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API")
        logger.info("Обработка ASSEMBLY_AI_API прошла успешно")
    except Exception as err:
        logger.error(f"Ошибка при обработке ASSEMBLY_AI_API: {err}")
        sys.exit()

    transcriber = aai.Transcriber()
    audio_url = (
        "/home/alexandervolzhanin/pet-project/CONSPECTIUS/app/audio/audio_message.ogg"
    )
    config = aai.TranscriptionConfig(language_code="ru")

    try:
        logger.info("Начало транскрибации")

        start_time = time.perf_counter()
        transcript = transcriber.transcribe(audio_url, config)
        end_time = time.perf_counter()

        logger.info("Конец транскрибации")
        logger.info(f"Время выполения: {end_time - start_time}")
        return transcript.text
        
    except Exception as err:
        logger.error(f"Ошибка при транскрибации: {err}")
        sys.exit()
