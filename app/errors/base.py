class BaseAppError(Exception):
    """
    Базовый класс для всех исключений в телеграмм боте.
    """

    def __init__(self, message="Произошла ошибка в телеграмм боте."):
        self.message = message
        super().__init__(self.message)
