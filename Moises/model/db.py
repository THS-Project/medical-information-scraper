import csv

import psycopg2


class Database:

    def __init__(self):
        self.credentials = self.database_cred()
        self.connection = psycopg2.connect(host=self.credentials['host'],
                                           database=self.credentials['database'],
                                           user=self.credentials['user'],
                                           password=self.credentials['password'],
                                           port=self.credentials['port'])

    def database_cred(self):
        with open('Moises/credentials.csv','r',newline='') as file:
            reader = csv.reader(file)
            next(reader)
            host, db, user, password, port = next(reader)
            db_dict = {"host": host, "database": db, "user": user,
                       "password": password, "port": port}
            return db_dict

    def close(self):
        self.connection.close()

