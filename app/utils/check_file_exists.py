import os


class CheckAudioConfig:
    """
    Класс для конфигурации пути загрузки аудиофайлов и поддерживаемых расширений.
    """

    SUPPORTED_EXTENSIONS: str = (
        ".3ga",
        ".8svx",
        ".aac",
        ".ac3",
        ".aif",
        ".aiff",
        ".alac",
        ".amr",
        ".ape",
        ".au",
        ".dss",
        ".flac",
        ".flv",
        ".m4a",
        ".m4b",
        ".m4p",
        ".m4r",
        ".mp3",
        ".mpga",
        ".ogg",
        ".oga",
        ".mogg",
        ".opus",
        ".qcp",
        ".tta",
        ".voc",
        ".wav",
        ".wma",
        ".wv",
    )
    standard_audio_upload_path = (
        "/CONSPECTIUS/shared_audio/{}"
    )

    def __init__(
        self,
        audio_upload_path: str = None,
        standart_supported_extensions: str = None,
    ):
        """Инициализация конфигурации.

        Args:
            audio_upload_path (str, optional): Путь к директории для загрузки файлов. Defaults to None.
            standart_supported_extensions (str, optional): Расширения, которые поддерживаются для аудиофайлов. Defaults to None.
        """
        self._audio_upload_path = (
            audio_upload_path or self.standard_audio_upload_path
        )
        self._supported_extensions = (
            standart_supported_extensions or self.SUPPORTED_EXTENSIONS
        )

    @property
    def audio_upload_path(self):
        return self._audio_upload_path

    @property
    def supported_extensions(self):
        return self._supported_extensions


class AudioManager:
    """
    Класс для управления аудиофайлами и проверки их существования.
    """

    def __init__(self, config: CheckAudioConfig):
        """Инициализация менеджера аудиофайлов.

        Args:
            config (CheckAudioConfig): Экземпляр класса конфигурации
        """
        self._config = config

    @property
    def config(self):
        return self._config

    def check_audio_file(self, telegram_id: int) -> str | FileNotFoundError:
        """Проверяет наличие аудиофайла для пользователя по его ID

        Args:
            telegram_id (int): ID пользователя, для которого проверяется файл.

        Raises:
            FileNotFoundError: Если файл не найден или имеет неподдерживаемое расширение.

        Returns:
            str | FileNotFoundError: Путь к файлу, если файл найден.
        """
        audio_path: str = self.config.audio_upload_path.format(
            str(telegram_id)
        )
        for extensions in self.config.supported_extensions:
            file_path = audio_path + extensions
            if os.path.isfile(file_path):
                return file_path

        else:
            raise FileNotFoundError(
                f"Файл {audio_path} для пользователя {telegram_id} не найден или имеет неподдерживаемое расширение."
            )


# Пример использования
# check_audio_config = CheckAudioConfig()
# audio_manager = AudioManager(check_audio_config)
# print(audio_manager.check_audio_file(857805093)) -> Если файл есть, то выведет путь к файлу,
#                                                     если нет - то вызовет ошибку
