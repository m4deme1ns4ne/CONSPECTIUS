from .base import BaseAppError


class UnsupportedExtension(BaseAppError):
    """
    Возникает, когда скинутый аудиофайл имеет не поддерживаемое расширение
    """

    def __init__(
        self, message="Скинутый аудиофайл имеет не поддерживаемое расширение"
    ):
        super().__init__(message)
