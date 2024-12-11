from .base import BaseAppError


class EmptyTextError(BaseAppError):
    """
    Возникает, когда переменная с текстом пустая.
    """

    def __init__(self, message="Переменная с текстом не может быть пустой"):
        super().__init__(message)
