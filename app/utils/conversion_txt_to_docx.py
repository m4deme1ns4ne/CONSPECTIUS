from docx import Document


class DocumentConfig:
    """
    Конфигурационный класс для управления путями сохранения файлов .docx.
    """

    def __init__(
        self,
        docx_output_path=None,
    ) -> None:
        """Инициализирует конфигурацию с заданным путём или использует путь по умолчанию.

        Args:
            docx_output_path (str | None): Пользовательский путь для сохранения .docx файлов.
        """
        self._docx_output_path = (
            docx_output_path
            or "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/{}.docx"
        )

    @property
    def docx_output_path(self):
        return self._docx_output_path

    @docx_output_path.setter
    def docx_output_path(self, new_docx_output_path: str):
        self._docx_output_path = new_docx_output_path


class DocumentManager:
    """Менеджер по работе с файлами .docx"""

    def __init__(self, config: DocumentConfig) -> None:
        self._config = config
        self._path_docx = None

    @property
    def config(self):
        return self._config

    @property
    def path_docx(self):
        return self._path_docx

    @path_docx.setter
    def path_docx(self, file_path: str):
        self._path_docx = file_path

    def txt_to_docx(self, text: str, telegram_id: int) -> None:
        """Сохраняет текст в файл по определённому пути и изменяет приватный атрибут _path_docx на значение пути нового файла

        Args:
            text (str): Строка, значение которой мы хотим записать в файл
        """
        # Создаем объект документа
        document = Document()

        # Добавляем содержимое переменной в документ
        document.add_paragraph(text)

        # Полный путь к файлу
        file_path: str = self.config.docx_output_path.format(str(telegram_id))

        # Сохраняем документ в файл с расширением .docx
        document.save(file_path)

        self.path_docx = file_path


# # Пример использования
# doc_config = DocumentConfig()
# doc_manager = DocumentManager(doc_config)
# doc_manager.txt_to_docx(
#     "Текст", 88417414
# ) # -> Новый файл с в диретории received_txt
# print(doc_manager.path_docx)
