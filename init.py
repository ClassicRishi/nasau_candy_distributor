import pymysql as mysql
import os
import streamlit as stl

class Connection:
    def __init__(self):
        self.connection = mysql.connect(
            charset=stl.secrets["CHARSET"],
            database=stl.secrets["DATABASE"],
            host=stl.secrets["HOST"],
            password=stl.secrets["PASSWORD"],
            port=stl.secrets["PORT"],
            user=stl.secrets["USER"]
        )

    def get_cursor(self):
        try:
            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print("There is an error !!")