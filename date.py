from datetime import datetime


def format_datetime(date: datetime.datetime) -> str:
    ordinal = get_ordinal(int(date.day))
    date_string = str(date.strftime('%A, %d{ordinal} %B %Y'))
    return date_string.format(ordinal=ordinal)


def get_ordinal(day: int) -> str:
    if 10 <= day % 100 < 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, "th")
