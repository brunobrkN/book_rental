import common.db_interaction
from common.interface import *

book_db = common.db_interaction.Database()
def rent_period():
    import datetime
    today = datetime.date.today()
    return_date = datetime.date(today.year, today.month, today.day + 14)
    return today, return_date

def rent_a_book(book_id):
    """
        → Realiza os registros no banco de dados para registro do livro e dados do cliente que locou.
    :param book_id: ID do livro dentro do banco de dados.
    :return:
    """
    id_available = book_db.id_exists(book_id=book_id)
    if id_available:
        try:
            book_title, books_available = availability(book_id=book_id)
        except TypeError:
            return
        else:
            if confirm('The return period is 14 days, do you confirm the selected book?(Y/N): ') in 'Y':
                today, period = rent_period()
                register_data = read_new_register(book_id=book_id, today=today, period=period)
                amount = register_data[2]
                if 0 < amount <= books_available:
                    book_db.insert(register_data, table_name='register')
                    book_db.stock_update(method=3, book_id=book_id, book_stock=amount)
                else:
                    adaptive_line(
                        f"Sorry, we don't have this amount of books! Please confirm in the stock column the amount available.")
            else:
                menu_title('Returning to main menu...')

def availability(book_id):
        """
            → Verifica disponibilidade do livro no estoque.
        :param book_id: ID do livro dentro do banco de dados.
        :return: Título e estoque do livro (se maior que 0)
        """
        book_title, books_available = \
            book_db.cursor.execute('SELECT title,stock FROM books WHERE id = :id', {'id': book_id}).fetchall()[0]
        if books_available == 0:
            return adaptive_line(f'Book "{book_title}" is not available!')
        else:
            adaptive_line(f'Book selected: "{book_title}"')
            return book_title, books_available

def return_book(rental_id,  book_id):
    """
        → Verifica o livro a ser devolvido e aciona a função stock(method = 1) para adicionar de volta a quantidade
         de livros ao estoque.
    :param book_id: ID do livro dentro do banco de dados.
    :param  rental_id: ID gerado ao locar livro.
    :return:
    """
    id_available = book_db.id_exists(book_id=book_id)

    if id_available:
        try:
            book_title = book_db.cursor.execute('SELECT title FROM books WHERE id = :id', {'id': book_id}).fetchone()[0]
            rented_books = book_db.cursor.execute('SELECT amount FROM register WHERE rental_id = :rental_id', {'rental_id': book_id}).fetchone()[0]
        except IndexError:
            adaptive_line('\33[31mPlease enter a valid ID.\33[m')
        except Exception as e:
            print(e)
        else:
            adaptive_line(f'Book selected: "{book_title}"')
            if confirm() in 'Y':
                book_db.remove(id = rental_id, table_name ='register')
                book_db.stock_update(method=1, book_id=book_id, book_stock = rented_books)
                adaptive_line('Book(s) were returned successfully!')
