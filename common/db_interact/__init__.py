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

    def _availability(self, book_id):
        book_title, books_available = \
        self.cursor.execute('SELECT title,stock FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
        if books_available == 0:
            print(f'Book "{book_title}" is not available!')
        else:
            print(f'Book selected: "{book_title}"')
            return book_title, books_available

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
        if method == 3:
            self.cursor.execute("UPDATE books SET stock = stock - :stock WHERE id = :id",
                                # método com valores designados explicitamente (mais legível)
                                {'stock': book_stock, 'id': book_id})
            self.conn.commit()
            print('Stock updated successfully!')

    def remove_book(self, book_id):
        self.cursor.execute("""DELETE FROM books WHERE id = :id""", {'id': book_id})
        self.conn.commit()
        print('Book removed successfully!')

    def show_list(self):
        line()
        print(f'{"ID":2}', f'{"Book name":<40}',f'{"Author":<15}',f'{"Stock":<8}')
        line()
        self.cursor.execute('SELECT id, title, author, stock FROM books WHERE stock != 0')
        books = self.cursor.fetchall()
        if len(books) == 0:
            print(f'No books found!'.center(70))
        else:
            self.cursor.execute('SELECT * FROM books')
            for book in books:
                book_id, title, author, stock= book
                print(f'{book_id:<2} {title:<40} {author:<15} {stock:<8}')

    def rent_a_book(self, book_id):
        book_title, books_available = self._availability(book_id = book_id)
        try:
                if confirm() in 'Y':
                    how_many = read_int('How many books do you want to rent?: ')
                    if 0 < how_many <= books_available:
                        self.stock(method=3, book_id=book_id, book_stock=how_many)
                        line()
                        print(f'{how_many} book(s) rented successfully!')
                    else:
                        print(
                            f"Sorry, we don't have this amount of books! Please confirm in the stock column the amount available.")
                else:
                    menu_title('Returning to menu...')
        except (TypeError,IndexError):
            line()
            print('\33[31mPlease enter a valid ID.\33[m'.center(70))

    def return_book(self, book_id):
        try:
            book_title = self.cursor.execute('SELECT title FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
            print(f'Book selected: "{book_title}"')
            book_return = read_int('How many books you want to return?: ')
            confirm()
            self.stock(method=1, book_id=book_id, book_stock = book_return)
            print('Book(s) were returned successfully!')
        except IndexError:
            line()
            print('\33[31mPlease enter a valid ID.\33[m'.center(70))

    def close_conn(self):
        if self.conn:
            print('Database connection closed.')
            self.conn.close()
