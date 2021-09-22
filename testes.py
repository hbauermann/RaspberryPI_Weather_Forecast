from datetime import datetime
import time


def time_update():
    date = datetime.now()
    end_date = date.strftime('%d/%m/%Y')
    time_now = date.strftime('%H:%M')
    date_time = time_now + ' ' + end_date
    return time_now, end_date

hora, data = time_update()
print(time_update()[1])
print(hora, data)