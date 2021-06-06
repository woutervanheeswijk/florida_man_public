from datetime import timedelta


def create_list_of_days(start_date, end_date, time_increment=timedelta(days=1)) -> None:
    """"Generate a list of days in day-month format"""
    date = start_date
    while date <= end_date:
        yield date.strftime("%d-%B")
        date += time_increment

    return None
