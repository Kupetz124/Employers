from datetime import datetime


def greet_user() -> str:
    """
    Формирует приветствие в зависимости от времени суток.

    """
    time_now = datetime.now().hour

    if 0 <= time_now < 6:
        return "Доброй ночи!"
    elif 6 <= time_now < 12:
        return "Доброе утро!"
    elif 12 <= time_now < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"
