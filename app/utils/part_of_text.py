def get_part_text(text: str, percent: int) -> str:
    """Получение части текста. Для удобства вводятся проценты.
    Например, если ввести 30, то метод выдаст первую треть текста и т.д.

    Args:
        text (str): Текст, часть которого нужно получить.
        percent (int): Процент, который нам нужен, отсчет начинается первого символа.

    Returns:
        str: _description_
    """

    # Если проценты не от 1 до 100, то выдаем ошибки
    if not (1 <= percent <= 100):
        raise ValueError("Проценты должны быть от 1 до 100")

    # Длина текста
    len_text = len(text)

    # Находим пропорции текста по пропорции
    num_parts = int((len_text * percent) / 100)

    num_parts = max(num_parts, 1) if len(text) > 0 else 0

    return text[:num_parts]


# # Пример использования:
# part_text = get_part_text(
#     text="Hi, my name is Sasha, I like cutlets.", percent=30
# )
# print(part_text)

# # Вывод в консоли: Hi, my name
