import os


def check_any_file_exists(directory_path):
    # Получаем список всех файлов в директории
    files = os.listdir(directory_path)

    # Проверяем, есть ли хотя бы один файл в директории
    if files:
        # Если есть, записываем путь к первому файлу в переменную
        first_file_path = os.path.join(directory_path, files[0])
        return first_file_path

    else:
        # Если файл не существует, возвращаем ошибку
        raise Exception("Файл не найден")
