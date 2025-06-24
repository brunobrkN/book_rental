import sqlite3
from common.interface import *

class Db:
    def __init__(self,db_name = 'library.db'):
        self.db_name = db_name
        self._connect()
        self._create_db()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER)""")

    def add_new(self,data):
        if not data:
            pass
        try:
            self.cursor.execute('INSERT INTO books (title,author,year) VALUES (?,?,?)', data)
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print(f'ERROr! {e} ')


    def show_list(self):
        line()
        print(f'{"ID":2}', f'{"Book name":<45}',f'{"Author":<20}')
        line()
        self.cursor.execute('SELECT id, title, author FROM books')
        books = self.cursor.fetchall()
        self.cursor.execute('SELECT * FROM books')
        for book in books:
            book_id, title, author = book
            print(f'{book_id:<2} {title:<45} {author:<20}')

    def rent(self, book_id):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        for i in range(1, len(books)+1):
            if book_id == i:
                print(f'Book selected: "{books[i-1][1]}"')
                if confirm() in 'Y':
                    print('works') # corrigir após adicionar dados de estoque no banco de dados.
                else:
                    menu_title('Returning to menu...')

    def close_conn(self):
        if self.conn:
            print('Database connection closed.')
            self.conn.close()
