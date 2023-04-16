from datetime import datetime


def format_datetime(date: datetime) -> str:
    day = int(date.day)
    ordinal = get_ordinal(day)
    return str(day) + ordinal + str(date.strftime(' %B %Y'))


def get_ordinal(day: int):
    if 10 <= day % 100 < 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, "th")
