from app.errors.empty_text import EmptyTextError


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
        self._text = text

    @property
    def text(self) -> str:
        """Геттер для получения текста"""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Сеттер для изменения текста"""
        if not isinstance(value, str):
            raise TypeError("Текст должен быть строкой.")
        self._text = value

    def split(self, n_parts: int) -> str:
        """
        Разделяет текст равные части.

        Return:
            str: Строка поделённая на несколько частей.

        Raises:
            EmptyTextError: Если текст пустой
        """
        if self.text is None:
            return EmptyTextError()

        n = len(self.text) // n_parts

        if n_parts == 3:
            part_1 = self.text[:n]
            part_2 = self.text[n : 2 * n]
            part_3 = self.text[2 * n :]

            return f"1.Начало: {part_1}.\n2.Середина: {part_2}.\n3.Конец: {part_3}."

        part_1 = self.text[:n]
        part_2 = self.text[n:]

        return f"1.Первая половина: {part_1}.\n2.Вторая половина: {part_2}."


# Пример использования:
# splitter = TextSplitter("abcdefghi")
# parts = splitter.split(n_parts=2)
# print(parts)  # Вывод: Первая половина: abcd.
#               #        Вторая половина: efghi.
