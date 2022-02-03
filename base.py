from peewee import *

db = SqliteDatabase('d_base.db')

class ZNO(Model):
    number = CharField()
    project = CharField()
    created_date = DateTimeField()
    sla_date = DateTimeField()
    closed = BooleanField()
    expired = BooleanField()

    class Meta:
        database = db

def add_zno(number, project, created_date, sla_date, closed, expired):
    zno = ZNO(
        number = number,
        project = project,
        created_date = created_date,
        sla_date = sla_date,
        closed = closed,
        expired = expired,
    )
    zno.save()

def clear():
    x = ZNO.delete()
    x.execute()


if __name__ == '__main__':
    db.connect()
    db.create_tables([ZNO,])
    db.close()
