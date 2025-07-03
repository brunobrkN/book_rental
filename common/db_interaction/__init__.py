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
        self._create_book_db()

    def _connect(self):
        """
            → Estabelece conexão com o banco de dados e define um cursor.
        :return:
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _create_book_db(self):
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

    def _create_register_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS register (
        id INTEGER NOT NULL,
        customer TEXT NOT NULL,
        amount INTEGER NOT NULL,
        acquisition TEXT NOT NULL,
        return TEXT NOT NULL)""")

    def _availability(self, book_id):
        """
            → Verifica disponibilidade do livro no estoque.
        :param book_id: ID do livro dentro do banco de dados.
        :return: Título e estoque do livro (se maior que 0)
        """
        book_title, books_available = \
        self.cursor.execute('SELECT title,stock FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
        if books_available == 0:
            return adaptive_line(f'Book "{book_title}" is not available!')
        else:
            adaptive_line(f'Book selected: "{book_title}"')
            return book_title, books_available

    def id_exists(self, book_id):
        id_available = self.cursor.execute('SELECT id FROM books').fetchall()
        try:
            for i in range(1, id_available[-1][0] + 1):
                if book_id == i:
                    id_available = True
                    return id_available
                else:
                    id_available = False
            adaptive_line('\33[31mERROR! ID not found!\33[m', True)
            return id_available
        except IndexError:
            adaptive_line('\33[31mERROR! No books found!\33[m', True)
            return False

    def add_new(self,data):
        """
            → Adiciona novo livro no banco de dados .
        :param* data: Dados lidos pelo comando new_book(): title,author,year,stock
        :return:
        """
        try:
            self.cursor.execute('INSERT INTO books (title,author,year,stock) VALUES (?,?,?,?)', data) #método com '?' como placeholder
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print(f'\33[31mERROR! {e}\33[m ')

    def stock(self, method, book_id, book_stock):
        """
            → Altera o estoque no banco de dados.
        :param method: Método de atualização
        :param book_id: ID do livro dentro do banco de dados.
        :param book_stock: Valor a ser alterado no estoque.
        :return:
        """
        id_available = self.id_exists(book_id=book_id)
        if id_available:
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
        id_available = self.id_exists(book_id=book_id)
        if id_available:
            self.cursor.execute(f"""DELETE FROM books WHERE id = :id""", {'id': book_id})
            self.conn.commit()
            print('Book removed successfully!')

    def show_list(self, actual_stock = 0):
        """
            → Exibe a lista de livros disponíveis (com estoque > 0)
        :return:
        """
        line()
        print(f'{"ID":2}', f'{"Book name":<40}',f'{"Author":<15}',f'{"Stock":<8}')
        line()
        self.cursor.execute('SELECT id, title, author, stock FROM books WHERE stock != :stock', {'stock': actual_stock})
        books = self.cursor.fetchall()
        if len(books) == 0:
            print(f'No books found!'.center(70))
        else:
            self.cursor.execute('SELECT * FROM books')
            for book in books:
                book_id, title, author, stock= book
                print(f'{book_id:<2} {title:<40} {author:<15} {stock:<8}')

    def rent_a_book(self, book_id, amount, customer):
        """
            → Aciona a função _availability() para verificação do estoque e faz a chamada da função stock(method = 3) para
            reduzir do estoque conforme quantidade informada pelo usuário. Informa erro e retorna ao menu caso seja informado
            o ID incorreto.
        :param book_id: ID do livro dentro do banco de dados.
        :param amount: Valor a ser alterado no estoque.
        :return:
        """
        id_available = self.id_exists(book_id=book_id)
        if id_available:
            try:
                book_title, books_available = self._availability(book_id=book_id)
            except TypeError:
                pass
            else:
                if confirm('The return period is 14 days, do you confirm the selected book?(Y/N): ') in 'Y':
                    if 0 < amount <= books_available:
                        self.add_to_register(book_id=book_id, amount=amount, customer = customer)
                        self.stock(method=3, book_id=book_id, book_stock=amount)
                    else:
                        adaptive_line(
                            f"Sorry, we don't have this amount of books! Please confirm in the stock column the amount available.")
                else:
                    menu_title('Returning to main menu...')

    def add_to_register(self, book_id, amount, customer):
        self._create_register_db()
        acquisition, return_date = self.rent_period()
        data = (book_id, customer,amount, acquisition, return_date)
        self.cursor.execute('INSERT INTO register (id, customer,amount, acquisition, return) VALUES (?,?,?,?,?)', data)
        self.conn.commit()

    def return_book(self, book_id,  customer):
        """
            → Verifica o livro a ser devolvido e aciona a função stock(method = 1) para adicionar de volta a quantidade
             de livros ao estoque.
        :param book_id: ID do livro dentro do banco de dados.
        :param rented_books: Quantos livros o cliente alugou.
        :param  customer: Nome do cliente que alugou
        :return:
        """
        id_available = self.id_exists(book_id=book_id)
        if id_available:
            try:
                book_title = self.cursor.execute('SELECT title FROM books WHERE id = :id', {'id': book_id}).fetchone()[0]
                rented_books = self.cursor.execute('SELECT amount FROM register WHERE id = :id AND customer = :customer', {'id': book_id,'customer' : customer}).fetchone()[0]
                print(rented_books)
            except IndexError:
                adaptive_line('\33[31mPlease enter a valid ID.\33[m')
            except Exception as e:
                print(e)
            else:
                adaptive_line(f'Book selected: "{book_title}"')
                if confirm() in 'Y':
                    self.remove_from_register(book_id, customer)
                    self.stock(method=1, book_id=book_id, book_stock = rented_books)
                    adaptive_line('Book(s) were returned successfully!')

    def remove_from_register(self, book_id, customer):
        rented_books = self.cursor.execute('SELECT amount FROM register WHERE id = :id AND customer = :customer', {'id': book_id,'customer' : customer}).fetchall()[0]
        print(rented_books)
        self.cursor.execute("""DELETE FROM register WHERE id = :id AND customer = :customer""", {'id': book_id, 'customer' : customer})
        self.conn.commit()

    def close_conn(self):
        """
        Fecha conexão com o banco de dados.
        :return:
        """
        if self.conn:
            adaptive_line('Database connection closed.')
            self.conn.close()

    @staticmethod
    def rent_period():
        import datetime
        today = datetime.date.today()
        return_date = datetime.date(today.year, today.month, today.day + 14)
        return today, return_date
