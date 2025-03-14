import re


def remove_markdown(text: str) -> str:
    """Убирает разметку markdown из текста, при этом сохраняя
    оригинальные переносы строк.

    Args:
        text (str): Текст, разметку markdown нужно убрать.

    Returns:
        str: Текст, без разметки markdown.
    """
    # Удаление заголовков (например, # Заголовок)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Удаление жирного и курсива (**жирный**, *курсив*)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)

    # Удаление ссылок и изображений, оставление текста ([текст](url) → текст)
    text = re.sub(r"!\[([^\]]+)\]\([^)]+\)", r"\1", text)  # Изображения
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # Ссылки

    # Удаление кода (`код` или ```код```)
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text, flags=re.DOTALL)

    # Удаление маркеров списков (*, -, +)
    text = re.sub(r"^[\*\-\+]\s+", "", text, flags=re.MULTILINE)

    # Удаление горизонтальных линий (---, ***, ___)
    text = re.sub(r"^[-*_]{3,}$", "", text, flags=re.MULTILINE)

    # Удаление цитат (> текст)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)

    # Удаление лишних переносов строк
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()


# Пример использования:
# input_text = """
# # Привет
# > Попробуй мои
# ### Мягкие французские булочек
# """
# text = remove_markdown(input_text)
# print(text) -> Привет
#                Попробуй мои
#                Мягкие французские булочек
