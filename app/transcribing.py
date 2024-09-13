import assemblyai as aai
import time
from loguru import logger
import os
from dotenv import load_dotenv


def convert_seconds(seconds):
    if seconds >= 60:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes} минут {round(remaining_seconds)} секунд"
    else:
        return f"{round(seconds)} секунд"

@logger.catch
def transcribing_aai() -> str:
    
    from handlers import telegram_id
    load_dotenv()

    download_path = f"/home/alexandervolzhanin/pet-project/CONSPECTIUS/app/audio/{telegram_id}.mp3"

    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API")
        logger.info("Обработка ASSEMBLY_AI_API прошла успешно")

    except Exception as err:
        logger.error(f"Ошибка при обработке ASSEMBLY_AI_API: {err}")

    transcriber = aai.Transcriber()
    audio_url = (download_path)
    config = aai.TranscriptionConfig(language_code="ru")

    try:
        logger.info("Начало транскрибации")

        start_time = time.perf_counter()
        transcript = transcriber.transcribe(audio_url, config)
        end_time = time.perf_counter()

        completion_time = end_time - start_time

        logger.info("Конец транскрибации")
        logger.info(f"Время выполения транскрибации: {convert_seconds(completion_time)}")

        try:
            os.remove(download_path)
            logger.info(f"Аудиофайл {telegram_id} удалён")
        except Exception as err:
            logger.error(f"Ошибка при удалении аудио: {err}")

        return transcript.text
        
    except Exception as err:
        logger.error(f"Ошибка при транскрибации: {err}")
