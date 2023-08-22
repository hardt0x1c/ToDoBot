from datetime import datetime, timedelta


def get_now_date():
    now_time = datetime.now().strftime('%d-%m-%y')
    return now_time


def get_week_dates():
    dates = []
    today = datetime.now().date()

    for _ in range(7):
        dates.append(today.strftime('%d-%m-%y'))
        today += timedelta(days=1)

    return dates
