from datetime import datetime


def get_now_date():
    now_time = datetime.now().strftime('%d-%m-%y')
    return now_time
