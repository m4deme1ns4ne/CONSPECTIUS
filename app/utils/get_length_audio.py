import warnings

from pydub import AudioSegment


# Подавление всех предупреждений
warnings.filterwarnings("ignore")


def get_length_audio(file_path_audio: str) -> str:
    """Функция для измерения длительности аудио

    Args:
        file_path_audio (str): Путь к аудио

    Returns:
        str: Параметры длительности аудио (минимальные, средние, максимальные)
    """
    audio = AudioSegment.from_file(file_path_audio)
    duration_in_seconds = len(audio) / 1000  # Длительность в секундах
    duration_in_minutes = duration_in_seconds / 60  # Длительность в минутах

    lenght_audio = int(round((duration_in_minutes)))

    if lenght_audio <= 30:
        return "low"
    if lenght_audio > 30 and lenght_audio <= 60:
        return "medium"
    if lenght_audio > 60:
        return "high"

    return lenght_audio


# Пример использования функции
# FILE_PATH_AUDIO = "..."
# print(get_length_audio(FILE_PATH_AUDIO)) # Вывод max_settings если > 60
