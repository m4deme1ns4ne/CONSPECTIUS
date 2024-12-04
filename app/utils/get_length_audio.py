import warnings
from pydub import AudioSegment

# Подавление всех предупреждений
warnings.filterwarnings("ignore")

def get_length_audio(file_path_audio: str) -> float:
    """Функция для измерения длительности аудио

    Args:
        file_path_audio (str): Путь к аудио

    Returns:
        float: Параметры длительности аудио (минимальные, средние, максимальные)
    """
    audio = AudioSegment.from_file(file_path_audio)
    duration_in_seconds = len(audio) / 1000  # Длительность в секундах
    duration_in_minutes = duration_in_seconds / 60  # Длительность в минутах
    
    lenght_audio = int(round((duration_in_minutes)))

    if lenght_audio <= 30:
        return "min_settings"
    if lenght_audio > 30 and lenght_audio <= 60:
        return "middle_settings"
    if lenght_audio > 60:
        return "max_settings"

    return lenght_audio

#Пример использования функции 

# FILE_PATH_AUDIO = "/Users/aleksandrvolzanin/pet_project/utils/testsadsadsa/Российский государственный педагогический университет им. А.И. Герцена 2.m4a"

# try:
#     print(get_length_audio(FILE_PATH_AUDIO)) -> max_settings (if > 60)
# except Exception as e:
#     print(f"Error: {e}")
