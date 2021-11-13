from datetime import datetime

date_format = "%Y-%m-%d %H:%M:%S.%f"

def convert_str_datetime(string_date: str):
    return datetime.strptime(
        string_date,
        date_format
    )


def convert_datetime_str(cdate: datetime):
    return cdate.strftime(date_format)
