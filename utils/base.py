import psycopg2

class Database:
    def __init__(self):
        self.__connection = self.__connect()

    def __connect(self):
        connection = psycopg2.connect(user = "postgres",
                                      password = "postgres",
                                      host = "database",
                                      port = "5432",
                                      database = "postgres")
        return connection

    def update(self, book):
        pass

    def test(self):
        print (self.__connection.get_dsn_parameters())
