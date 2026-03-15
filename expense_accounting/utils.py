import datetime


def check_date_satisfy_given_date_format(date_str: str, date_format: str) -> str:
    try:
        datetime.datetime.strptime(date_str, date_format)

    except (TypeError, ValueError):
        raise ValueError(
            f"date string {date_str!r} doesn't match date format {date_format!r}"
        ) from None

    return date_str
