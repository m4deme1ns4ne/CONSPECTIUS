import os

from docx import Document


def txt_to_docx(text: str) -> None:
    """Сохраняет текст в файл по определённому пути

    Args:
        text (str): Строка, значение которой мы хотим записать в файл
    """

    # Временно
    FILE_URL = (
        "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/"
    )
    FILE_NAME = "input_file.docx"

    # Создаем объект документа
    doc = Document()

    # Добавляем содержимое переменной в документ
    doc.add_paragraph(text)

    # Полный путь к файлу
    file_path = os.path.join(
        FILE_URL,
        FILE_NAME,
    )

    # Сохраняем документ в файл с расширением .docx
    doc.save(file_path)
