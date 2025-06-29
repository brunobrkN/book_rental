import sqlite3
from common.interface import *

class Db:
    def __init__(self,db_name = 'library.db'):
        """
            → Estabelece conexão e cria base de dados.
        :param db_name: Nome do arquivo de dados.
        """
        self.db_name = db_name
        self._connect()
        self._create_db()

    def _connect(self):
        """
            → Estabelece conexão com o banco de dados e define um cursor.
        :return:
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _create_db(self):
        """
            → Cria a tabela no banco de dados.
        :return:
        """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        stock INTEGER NOT NULL)""")

    def _availability(self, book_id):
        """
            → Verifica disponibilidade do livro no estoque.
        :param book_id: ID do livro dentro do banco de dados.
        :return: Título e estoque do livro (se maior que 0)
        """
        try:
            book_title, books_available = \
            self.cursor.execute('SELECT title,stock FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
            if books_available == 0:
                return adaptive_line(f'Book "{book_title}" is not available!')
            else:
                adaptive_line(f'Book selected: "{book_title}"')
                return book_title, books_available
        except IndexError:
            return adaptive_line('No books available!')


    def add_new(self,data):
        """
            → Adiciona novo livro no banco de dados .
        :param data: Dados lidos pelo comando new_book(): title,author,year,stock
        :return:
        """
        try:
            self.cursor.execute('INSERT INTO books (title,author,year,stock) VALUES (?,?,?,?)', data) #método com '?' como placeholder
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print(f'\33[31mERROR! {e}\33[m ')

    def stock(self, method, book_id, book_stock):
        """
            → Atualiza a coluna estoque do livro informado (id) no banco de dados .
        :param method: Método de atualização:
        1- Soma com o estoque atual
        2- Substitui o estoque atual
        3- Subtrai do estoque atual
        :param book_id: ID do livro dentro do banco de dados.
        :param book_stock: Quantidade a ser adicionado/ subtraido / substituido do estoque.
        :return:
        """
        match method:
            case 1:
                self.cursor.execute("UPDATE books SET stock = stock + :stock WHERE id = :id", #método com valores designados explicitamente (mais legível)
                                    {'stock': book_stock, 'id': book_id})
                print('Stock updated successfully!')
            case 2:
                self.cursor.execute("UPDATE books SET stock = :stock WHERE id = :id",
                                    {'stock': book_stock,'id': book_id})
                print('Stock replaced successfully!')
            case 3:
                self.cursor.execute("UPDATE books SET stock = stock - :stock WHERE id = :id",
                                    {'stock': book_stock, 'id': book_id})
                print('Stock updated successfully!')
        self.conn.commit()

    def remove_book(self, book_id):
        """
            → Remove todos os dados livro selecionado no banco de dados.
        :param book_id: ID do livro dentro do banco de dados.
        :return:
        """
        self.cursor.execute("""DELETE FROM books WHERE id = :id""", {'id': book_id})
        self.conn.commit()
        print('Book removed successfully!')

    def show_list(self):
        """
            → Exibe a lista de livros disponíveis (com estoque > 0)
        :return:
        """
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
        """
            → Aciona a função _availability() para verificação do estoque e faz a chamada da função stock(method = 3) para
            reduzir do estoque conforme quantidade informada pelo usuário.
        :param book_id: ID do livro dentro do banco de dados.
        :return:
        """

        try:
            book_title, books_available = self._availability(book_id=book_id)
            if confirm() in 'Y':
                how_many = read_int('How many books do you want to rent?: ')
                if 0 < how_many <= books_available:
                    self.stock(method=3, book_id=book_id, book_stock=how_many)
                    adaptive_line(f'{how_many} book(s) rented successfully!')
                else:
                    adaptive_line(
                        f"Sorry, we don't have this amount of books! Please confirm in the stock column the amount available.")
            else:
                menu_title('Returning to main menu...')
        except (TypeError,IndexError):
            adaptive_line('\33[31mERROR! ID not found.\33[m')

    def return_book(self, book_id):
        """
            → Verifica o livro a ser devolvido e aciona a função stock(method = 1) para adicionar de volta a quantidade
             de livros ao estoque.
        :param book_id: ID do livro dentro do banco de dados.
        :return:
        """
        try:
            book_title = self.cursor.execute('SELECT title FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
            adaptive_line(f'Book selected: "{book_title}"')
            book_return = read_int('How many books you want to return?: ')
            confirm()
            self.stock(method=1, book_id=book_id, book_stock = book_return)
            adaptive_line('Book(s) were returned successfully!')
        except IndexError:
            adaptive_line('\33[31mPlease enter a valid ID.\33[m')

    def close_conn(self):
        """
        Fecha conexão com o banco de dados.
        :return:
        """
        if self.conn:
            adaptive_line('Database connection closed.')
            self.conn.close()
