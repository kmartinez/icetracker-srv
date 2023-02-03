from peewee import *

# Placeholder database
db = MySQLDatabase(None)

# Model representing tracker_data table
class TrackerData(Model):
    id = AutoField() # An Integer, auto increment primary key
    rover_id = IntegerField(unique=True, null=True)
    timestamp = DateTimeField(unique=True, null=True)
    longitude = DoubleField(null=True)
    latitude = DoubleField(null=True)
    altitude = DoubleField(null=True)
    quality = IntegerField()
    hdop = FloatField()
    sats = IntegerField(null=True)
    temperature = FloatField()

    # Maps column names to columns within the data model
    @staticmethod
    def get_column_map():
        return { column.column_name: column for column in TrackerData._meta.sorted_fields }

    class Meta:
        database = db
        table_name = "tracker_data"

# Model representing tracker_devices table
class TrackerDevices(Model):
    rover_id = AutoField() # An Integer, auto increment primary key
    imei = CharField(15)
    Notes = CharField(250)
    Glacier = CharField(40)

    # Maps column names to columns within the data model
    def get_column_map():
        return { column.column_name: column for column in TrackerDevices._meta.sorted_fields }

    class Meta:
        database = db
        table_name = "tracker_devices"

# Model representing api_keys table
class ApiKeys(Model):
    id = AutoField() # An Integer, auto increment primary key
    api_key = CharField(255)

    # Maps column names to columns within the data model
    def get_column_map():
        return { column.column_name: column for column in ApiKeys._meta.sorted_fields }

    class Meta:
        database = db
        table_name = "api_keys"