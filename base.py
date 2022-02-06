from peewee import *
import datetime

db = SqliteDatabase('d_base.db')

class ZNO(Model):
    project = CharField()
    sla_date = DateTimeField()
    receipt_date = DateTimeField()
    closed = BooleanField()
    expired = BooleanField()

    class Meta:
        database = db

def add_zno(project, sla_date, receipt_date, closed, expired):
    zno = ZNO(
        project = project,
        sla_date = sla_date,
        receipt_date = receipt_date,
        closed = closed,
        expired = expired,
    )
    zno.save()

def clear():
    x = ZNO.delete()
    x.execute()

'''Заполняем из базы форму отчета и выводим в консоль'''
def add_data_to_report_form():
    datetime_now = '00:00:00 ' + datetime.datetime.now().strftime("%d.%m.%y")
    datetime_now = datetime.datetime.strptime(datetime_now, '%H:%M:%S %d.%m.%y')

    full_text = f'    Челябинская обл.	{datetime.datetime.now().strftime("%d.%m.%y")}'

    all = ZNO.select()

    project = set()

    for i_project in all:
        project.add(i_project.project)

    project = list(project)
    
    for i in range(len(project)):
        full_text = full_text + f'''\n
        Проект:	{project[i]}	
    Поступило ЗНО:	{len(ZNO.select().where((ZNO.project == project[i]) & (ZNO.receipt_date > datetime_now)))}	
    Закрыто ЗНО:	{len(ZNO.select().where((ZNO.project == project[i]) & (ZNO.closed == 1)))}	(в том числе с просроком: {len(ZNO.select().where((ZNO.project == project[i]) & (ZNO.closed == 1) & (ZNO.expired == 1)))})
    Осталось ЗНО:	{len(ZNO.select().where((ZNO.project == project[i]) & (ZNO.closed == 0)))}	(в том числе с просроком: {len(ZNO.select().where((ZNO.project == project[i]) & (ZNO.closed == 0) & (ZNO.expired == 1)))})'''

    print(full_text + '\n\nШтат 7 инженеров ')


if __name__ == '__main__':
    db.connect()
    db.create_tables([ZNO,])
    db.close()
