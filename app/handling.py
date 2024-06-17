from openai import OpenAI
import os
from dotenv import load_dotenv
from loguru import logger
import httpx
import sys

from promt_for_gpt import role_system, role_user


@logger.catch
def handling(text: str) -> str: 
    load_dotenv()
    try:
        client = OpenAI(api_key=os.getenv("API_OPEN_AI"),
                        http_client=httpx.Client(
                            proxies=os.getenv("PROXY"),
                            transport=httpx.HTTPTransport(local_address="0.0.0.0")
                        ))
        logger.info("API_OPEN_AI обработан")

    except Exception as err:
        logger.error(f"Ошибка при получении API_OPEN_AI: {err}")
        sys.exit()
    
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": f"{role_user} {text}"}
                 ])
        
        logger.info("Обработка файла завершена")
        res = completion.choices[0].message.content
        return res

    except Exception as err:
        logger.error(f"Ошибка при обработке запроса: {err}")
        sys.exit()
