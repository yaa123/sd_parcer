from base import *
from prettytable import PrettyTable
import datetime

date_now = datetime.datetime.now().strftime('%m.%d.%y')

mytable = PrettyTable()
mytable.field_names = ['', 'Челябинская обл.', date_now]

all = ZNO.select()

project = set()

for i_project in all:
    project.add(i_project.project)


project = list(project)

x, y, z = [], [], []

for i in project:
    x.append(i)
    zno = ZNO.select().where(ZNO.project == i)
    y.append(len(zno))
    expired = ZNO.select().where(ZNO.project == i, ZNO.expired == 1)
    if expired:
        z.append(len(expired))
    else:
        z.append(0)

for i in range(len(x)):
    mytable.add_row([x[i], y[i], z[i]])

print(mytable)
