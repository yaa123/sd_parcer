import datetime
import pytz

tz_yek = pytz.timezone('Asia/Yekaterinburg')

a = '14:12:48 30.12.2021'
b = '14:13:48 30.12.2021'

try:
    a_dt = datetime.datetime.strptime(a, '%H:%M:%S %d.%m.%Y')
    b_dt = datetime.datetime.strptime(str(datetime.datetime.now(tz_yek))[:-13], '%Y-%m-%d %H:%M:%S')
    delta = a_dt - b_dt
    if str(delta)[0] == '-':
        expired = 1
    else:
        expired = 0
except ValueError:
    expired = '0'

print(delta)

print(datetime.date.today().strftime('%d.%m.%Y'))
