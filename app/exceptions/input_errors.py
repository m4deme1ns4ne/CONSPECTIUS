from .base import BaseAppError


class EmptyTextError(BaseAppError):
    """
    Raised when input text is empty.
    """

    def __init__(self, message="Input text cannot be empty."):
        super().__init__(message)
