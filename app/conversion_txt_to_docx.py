from docx import Document
import os


def txt_to_docx(text: str) -> None:

    from handlers import telegram_id

    # Создаем объект документа
    doc = Document()

    # Добавляем содержимое переменной в документ
    doc.add_paragraph(text)

    # Определяем путь к папке
    folder_path = f'/home/alexandervolzhanin/pet-project/CONSPECTIUS/app/received_txt/'

    # Полный путь к файлу
    file_path = os.path.join(folder_path, f"{telegram_id}.docx")

    # Сохраняем документ в файл с расширением .docx
    doc.save(file_path)
