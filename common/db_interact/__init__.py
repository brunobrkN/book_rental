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
        year INTEGER NOT NULL,
        stock INTEGER NOT NULL)""")

    def add_new(self,data):
        if not data:
            pass
        try:
            self.cursor.execute('INSERT INTO books (title,author,year,stock) VALUES (?,?,?,?)', data) #método com '?' como placeholder
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print(f'\33[31mERROR! {e}\33[m ')

    def stock(self, method, book_id, book_stock):
        if method == 1:
            self.cursor.execute("UPDATE books SET stock = stock + :stock WHERE id = :id", #método com valores designados explicitamente (mais legível)
                                {'stock': book_stock, 'id': book_id})
            self.conn.commit()
            print('Stock updated successfully!')
        if method == 2:
            self.cursor.execute("UPDATE books SET stock = :stock WHERE id = :id",
                                {'stock': book_stock,'id': book_id})
            self.conn.commit()
            print('Stock replaced successfully!')
    def show_list(self):
        line()
        print(f'{"ID":2}', f'{"Book name":<40}',f'{"Author":<15}',f'{"Stock":<8}')
        line()
        self.cursor.execute('SELECT id, title, author, stock FROM books')
        books = self.cursor.fetchall()
        if len(books) == 0:
            print(f'No books found!'.center(70))
        else:
            self.cursor.execute('SELECT * FROM books')
            for book in books:
                book_id, title, author, stock= book
                print(f'{book_id:<2} {title:<40} {author:<15} {stock:<8}')

    def rent(self, book_id):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        for i in range(1, len(books)+1):
            if book_id == i:
                print(f'Book selected: "{books[i-1][1]}"')
                if confirm() in 'Y':
                    more_than_one = confirm('Do you want to rent more than 1 book?(Y/N): ')
                    if more_than_one in 'Y':
                        how_many = read_int('how many books do you want to rent?')
                        self.stock(method = 1, book_id=book_id, book_stock=-how_many)
                        line()
                        print(f'{-how_many} books rented successfully!')
                    else:
                        how_many = -1
                        self.stock(method = 1, book_id=book_id, book_stock=how_many)
                        line()
                        print('Book rented successfully!')
                else:
                    menu_title('Returning to menu...')

    def close_conn(self):
        if self.conn:
            print('Database connection closed.')
            self.conn.close()
