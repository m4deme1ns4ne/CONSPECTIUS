import tiktoken


def count_tokens(prompt, model="gpt-4"):
    # Инициализация кодировщика для нужной модели
    encoding = tiktoken.encoding_for_model(model)
    
    # Кодирование текста в токены
    tokens = encoding.encode(prompt)
    
    # Возвращаем количество токенов
    return len(tokens)
