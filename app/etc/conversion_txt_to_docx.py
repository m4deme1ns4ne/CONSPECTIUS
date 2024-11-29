from docx import Document
import os


def txt_to_docx(text: str) -> None:

    # Создаем объект документа
    doc = Document()

    # Добавляем содержимое переменной в документ
    doc.add_paragraph(text)

    # Полный путь к файлу
    file_path = os.path.join("/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/", f"input_file.docx")

    # Сохраняем документ в файл с расширением .docx
    doc.save(file_path)
