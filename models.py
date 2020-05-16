import peewee

db = peewee.SqliteDatabase(
    'boone_county_jail.db',
    pragmas={'foreign_keys': 1}
)



class Detainee_Info(peewee.Model):
    detainee_id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
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
    detainee_id = peewee.IntegerField()
    name = peewee.CharField()
    case_num = peewee.CharField()
    charge_description = peewee.CharField()
    charge_status = peewee.CharField()
    bail_amount = peewee.CharField()
    bond_type = peewee.CharField()
    court_date = peewee.DateField()
    court_time = peewee.TimeField()
    court_of_jurisdiction = peewee.CharField()

    class Meta:
        database = db



db.connect()
db.create_tables([Detainee_Info, Detainee_Charges])
