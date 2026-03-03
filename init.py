import pymysql as mysql
import os

class Connection:
    def __init__(self):
        self.connection = mysql.connect(
            charset=os.getenv("CHARSET"),
            database=os.getenv("DATABASE"),
            host=os.getenv("HOST"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("PORT"),
            user=os.getenv("USER")
        )

    def get_cursor(self):
        try:
            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print("There is an error !!")