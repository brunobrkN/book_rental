import sqlite3
from common.interface import *

class Db:
    def __init__(self,db_name = 'library.db'):
        self.chart = None
        self.conn = None
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.chart = self.conn.cursor()

    def create_db(self,data):
        self.chart.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER)""")
        self.chart.execute('INSERT INTO books (title,author,year) VALUES (?, ?, ?)', data)
        self.conn.commit()
        self.close_conn()

    def add_new(self,data):
        try:
            self.chart.execute('INSERT INTO books (title,author,year) VALUES (?,?,?)', data)
            self.conn.commit()
            self.close_conn()
        except:
            print('\33[31mERROR! Database not found.\33[m')
            menu_title('New database created.')
            self.create_db(data=data)
