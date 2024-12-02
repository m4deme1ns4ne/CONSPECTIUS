class BaseAppError(Exception):
    """
    Базовый класс для всех исключений, специфичных для телеграмм бота.

    Атрибуты:
        message (str): Сообщение об ошибке.

    Аргументы:
        message (str, optional): Сообщение об ошибке. По умолчанию "Произошла ошибка в телегрмм боте.".
    """
    def __init__(self, message="Произошла ошибка в телегрмм боте."):
        self.message = message
        super().__init__(self.message)
