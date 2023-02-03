import pymysql

class Database:
    def __init__(self):
        self.connect()

    # Connects to the test database
    def connect(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='iceland',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Database connected")

    # Delete the database
    def drop(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS iceland")
        self.connection.commit()
        print("Database dropped")

    # Re-create the database
    def initialise(self):
        with self.connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE iceland")
            cursor.execute("USE iceland")
        self.connection.commit()
        print("Database initialised")

    # Sets the SQL schema of the database
    def set_schema(self):
        with self.connection.cursor() as cursor:
            with open("tests\\unit\\schema.sql", "r") as f:
                sql = f.read()
                sql = sql.splitlines()
                sql = filter(lambda line: not line == "" and not line.startswith("--"), sql)
                sql = "".join(sql)
                sql = sql.split(";")[:-1]
                for s in sql:
                    #print(f"EXECUTING STATEMENT: {s}")
                    cursor.execute(s)
        self.connection.commit()
        print("Database schema set")

    # Registers an API key to be used for requests during testing
    def register_test_api_key(self):
        with self.connection.cursor() as cursor:
            cursor.execute("USE iceland")
            cursor.execute("INSERT INTO api_keys (api_key) VALUES ('fc2fb108fc2a781c2956188b6a96704ebdf9ae60e2384e3367b151585acbcd5742a1eff19e2ceca7e744568197eb9bef55dfe3ccb37ed01ec87e3fecfafaf167')")
        self.connection.commit()
        print("Test API key registered")

    # Fully drops the database and creates schema from SQL file
    def hard_reset(self):
        self.drop()
        self.initialise()
        self.set_schema()
        self.register_test_api_key()

    # Deletes data from tables quickly
    def soft_reset(self):
        with self.connection.cursor() as cursor:
            cursor.execute("USE iceland")
            cursor.execute("SET foreign_key_checks = 0")
            cursor.execute("TRUNCATE tracker_data")
            cursor.execute("TRUNCATE tracker_devices")
            cursor.execute("SET foreign_key_checks = 1")
            cursor.execute("ALTER TABLE tracker_data AUTO_INCREMENT = 0")
            cursor.execute("ALTER TABLE tracker_devices AUTO_INCREMENT = 0")