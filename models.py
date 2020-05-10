import peewee

db = peewee.SqliteDatabase(
    'detainee_info.db',
    pragmas={'foreign_keys': 1}
)



class Detainee_Info(peewee.Model):
    name = peewee.CharField(primary_key=True)
    height = peewee.CharField()
    weight = peewee.FloatField()
    sex = peewee.CharField()
    eyes = peewee.CharField()
    hair = peewee.CharField()
    race = peewee.CharField()
    age = peewee.IntegerField()
    city = peewee.CharField()
    state = peewee.CharField()

    class Meta:
        database = db

class Detainee_Charges(peewee.Model):
    name = peewee.ForeignKeyField(
        Detainee_Info,
        backref='charges',
        column_name='name',
    )
    case_num = peewee.CharField(primary_key=True)
    charge_description = peewee.CharField()
    charge_status = peewee.CharField()
    bail_amount = peewee.CharField()
    bond_type = peewee.CharField()
    court_date = peewee.DateField()
    court_time = peewee.TimeField()
    court_jur = peewee.CharField()

    class Meta:
        database = db



db.connect()
db.create_tables([Detainee_Info, Detainee_Charges])
