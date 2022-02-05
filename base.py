from peewee import *

db = SqliteDatabase('d_base.db')

class ZNO(Model):
    project = CharField()
    sla_date = DateTimeField()
    closed = BooleanField()
    expired = BooleanField()

    class Meta:
        database = db

def add_zno(project, sla_date, closed, expired):
    zno = ZNO(
        project = project,
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
