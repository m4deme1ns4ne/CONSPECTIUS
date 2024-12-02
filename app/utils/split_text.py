from ..exceptions.input_errors import EmptyTextError


class TextSplitter:
    """
    Вспомогательный класс для разделения текста на три равные части.
    """

    def __init__(self, text: str) -> None:
        """
        Инициализирует TextSplitter текстом, который нужно разделить.

        Arguments:
            text (str): Текст, который нужно разделить на три части.
        """
        if not isinstance(text, str):
            raise TypeError("Входные данные должны быть строкой.")
        self.text = text

    def split(self) -> tuple[str, str, str]:
        """
        Разделяет текст на три примерно равные части.

        Return:
            tuple[str, str, str]: Три части текста в виде строк.

        Raises:
            EmptyTextError: Если текст пустой
        """
        if self.text is None:
            return EmptyTextError()

        n = len(self.text)

        # Вычисление индексов разделения
        part_size = n // 3
        remainder = n % 3

        # Корректировка индексов разделения для распределения остатка
        split_1 = part_size + (1 if remainder > 0 else 0)
        split_2 = split_1 + part_size + (1 if remainder > 1 else 0)

        # Выполнение разделения
        part_1 = self.text[:split_1]
        part_2 = self.text[split_1:split_2]
        part_3 = self.text[split_2:]

        return f"1. {part_1}", f"2. {part_2}", f"3. {part_3}"

    def __repr__(self) -> str:
        """
        Возвращает строковое представление экземпляра TextSplitter.

        Возвращает:
            str: Представление объекта.
        """
        return f"TextSplitter(text='{self.text[:10]}...')"

# Пример использования:
# splitter = TextSplitter("abcdefghi")
# parts = splitter.split()
# print(parts)  # Вывод: ('abc', 'def', 'ghi')
