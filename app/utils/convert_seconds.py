def convert_seconds(seconds):
    if seconds >= 60:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes} минут {round(remaining_seconds)} секунд"
    else:
        return f"{round(seconds)} секунд"
