import os


def check_any_file_exists(directory_path: str) -> str | FileNotFoundError:
    # Функция временная и не подходит для большого кол-ва пользователей
    """Находит первый файл в директории и записывает его переменную

    Args:
        directory_path (str): Путь в директорию

    Raises:
        FileNotFoundError: Если файла нету

    Returns:
        str | FileNotFoundError: Путь к файлу
    """
    # Получаем список всех файлов в директории
    files = os.listdir(directory_path)

    # Проверяем, есть ли хотя бы один файл в директории
    if files:
        # Если есть, записываем путь к первому файлу в переменную
        first_file_path = os.path.join(directory_path, files[0])
        return first_file_path

    else:
        # Если файл не существует, возвращаем ошибку
        raise FileNotFoundError("Файл не найден")
