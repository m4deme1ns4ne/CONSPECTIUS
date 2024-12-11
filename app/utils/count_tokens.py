import tiktoken


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Возвращает кол-во токенов

    Args:
        text (str): Текст, кол-во токенов которого нудно посчитать
        model (str, optional): Модель нейросети, для который мы хотим посчитать токены. Defaults to "gpt-4o".

    Returns:
        int: Число токенов
    """
    # Инициализация кодировщика для нужной модели
    encoding = tiktoken.encoding_for_model(model)

    # Кодирование текста в токены
    tokens = encoding.encode(text)

    # Возвращаем количество токенов
    return len(tokens)
