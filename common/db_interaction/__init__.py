import sqlite3
from common.interface import *

class Database:
    def __init__(self,db_name = 'library.db'):
        """
            → Estabelece conexão e cria base de dados.
        :param db_name: Nome do arquivo de dados.
        """
        self.db_name = db_name
        self._connect()
        self._create_table()
        self._create_table(table_name='register')

    def _connect(self):
        """
            → Estabelece conexão com o banco de dados e define um cursor.
        :return:
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _create_table(self, table_name ='books'):
        """
                            → Cria a tabela no banco de dados.
                        :return:
                        """
        column_0, column_1, column_2, column_3, column_4, column_5 = self.sql_args(table_name)
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        {column_0} INTEGER PRIMARY KEY AUTOINCREMENT,
        {column_1} TEXT NOT NULL,
        {column_2} TEXT NOT NULL,
        {column_3} INTEGER NOT NULL,
        {column_4} INTEGER NOT NULL,
        {column_5} INTEGER NOT NULL)""")
        self.conn.commit()

    def insert(self, data, table_name = 'books'):
        """
            → Adiciona novo livro no banco de dados .
        :param* data: Dados lidos pelo comando new_book(): title,author,year,stock
        :return:
        """
        column_0, column_1, column_2, column_3, column_4, column_5 = self.sql_args(table_name)
        columns = (column_1 + column_2 + column_3 + column_4 + column_5).replace(' ', ',')
        placeholders = ','.join('?' * len(columns.split(',')))
        try:
            self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', data) #método com '?' como placeholder
            self.conn.commit()
        except (sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
            return print(f'\33[31mERROR! {e}\33[m ')

    def id_exists(self, book_id, table_name='books'):
        column_0, column_1, column_2, column_3, column_4, column_5 = self.sql_args(table_name)
        id_available = self.cursor.execute(f'SELECT {column_0} FROM {table_name} WHERE {column_0} = {book_id} ').fetchall()
        if len(id_available) > 0:
            exists = True
        else:
            print('\33[31mERROR! ID not found!\33[m ')
            exists = False
        return exists

    def stock_update(self, method, book_id, book_stock):
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
                    operator = 'stock +'
                case 2:
                    operator = ''
                case 3:
                    operator = 'stock -'
            try:
                self.cursor.execute(f"UPDATE books SET stock = {operator} :stock WHERE id = :id",
                                    {'stock': book_stock, 'id': book_id})
                self.conn.commit()
            except (sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
                print(f'\33[31mERROR! {e}\33[m ')

    def remove(self, id, table_name ='books'):
        """
            → Remove todos os dados do id selecionado no banco de dados.
        :param id: ID usado para identificar o livro/registrar dados da locação.
        :return:
        """
        column_0, column_1, column_2, column_3, column_4, column_5 = self.sql_args(table_name)
        id_available = self.id_exists(book_id = id)
        if id_available:
            verify_column = column_0
            self.cursor.execute(f"""DELETE FROM {table_name} WHERE {verify_column} = :id""", {'id': id})
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

    def close_conn(self):
        """
        Fecha conexão com o banco de dados.
        :return:
        """
        if self.conn:
            adaptive_line('Database connection closed.')
            self.conn.close()

    @staticmethod
    def sql_args(table_name='books'):
        if table_name == 'books':
            columns = ('id ', 'title ', 'author ', 'year ', 'stock ', 'price')
        elif table_name == 'register':
            columns = ('rental_id ', 'customer ', 'book_id ', 'amount ','acquisition ', 'return')
        else:
            return print('\33[31mERROR! Table is not in database.\33[m')
        return columns
