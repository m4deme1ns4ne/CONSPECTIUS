from .base import BaseAppError


class FileNotAudio(BaseAppError):
    """
    Возникает, когда скинутый файл не является аудио
    """

    def __init__(self, message="Скинутый файл не является аудио"):
        super().__init__(message)
