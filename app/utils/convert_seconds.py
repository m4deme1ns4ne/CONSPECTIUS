def convert_seconds(seconds: int) -> str:
    """Возвращает строку с понятным отображением времени.

    Args:
        seconds (int): Секунды

    Returns:
        str: Строка с кол-вом секунд | минут.
    """
    if seconds >= 60:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes} минут {round(remaining_seconds)} секунд"
    else:
        return f"{round(seconds)} секунд"
