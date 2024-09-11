from openai import OpenAI
import tiktoken
from dotenv import load_dotenv
from loguru import logger
import httpx
from logger import file_logger
import os

from promt_for_gpt import role_system, role_user_0, role_user_1


def handler_gpt(text: str, promt: str) -> str: 

    load_dotenv()

    try:
        client = OpenAI(api_key=os.getenv("API_OPEN_AI"),
                        http_client=httpx.Client(
                            proxies=os.getenv("PROXY"),
                            transport=httpx.HTTPTransport(local_address="0.0.0.0")
                        ))
        logger.info("API_OPEN_AI обработан")

    except Exception as err:
        logger.info(f"Ошибка при получении API_OPEN_AI: {err}")
    
    try:
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": f"{promt} {text}"}
                 ])
        
        logger.info("Обработка файла завершена")
        res = completion.choices[0].message.content
        return res

    except Exception as err:
        logger.info(f"Ошибка при обработке запроса: {err}")


def split_text(text, max_tokens=16384):
    enc = tiktoken.get_encoding("cl100k_base")  # или другой подходящий для вашей модели
    tokens = enc.encode(text)
    
    # Разбиваем токены на части, каждая из которых не превышает max_tokens
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    
    # Декодируем обратно в текст
    return [enc.decode(chunk) for chunk in chunks]


def count_tokens(prompt, model="gpt-4"):
    # Инициализация кодировщика для нужной модели
    encoding = tiktoken.encoding_for_model(model)
    
    # Кодирование текста в токены
    tokens = encoding.encode(prompt)
    
    # Возвращаем количество токенов
    return len(tokens)


@logger.catch
def handling(text: str) -> str:

    file_logger()
    
    split_texts = split_text(text)
    ansver = ""

    for i, chunk in enumerate(split_texts):
        if i == 0:
            res = handler_gpt(chunk, role_user_0)
        else:
            res = handler_gpt(chunk, role_user_1)
        ansver += f"{res + '\n'}"

    model_name = "gpt-4o-mini"  # Укажите модель, которую вы используете
    token_count = count_tokens(text, model=model_name)
    
    logger.info(f"Количество токенов для запроса: {token_count}")

    return ansver
