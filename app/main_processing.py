from handling import handling
from logger import file_logger
from transcribing import transcribing_aai


from loguru import logger
import sys


@logger.catch
def main_processing() -> str:
    file_logger()
    try:
        res = transcribing_aai()
        result = handling(res)
        logger.info("Ответ получен и выведен")
        return result
    
    except Exception as err:
        logger.error(f'Ошибка при получении ответа: {err}')
        sys.exit()
