from common import text_formatter as form, read
from common.db_interaction import DbInteraction as Db


class BookManager(Db):

    def show_list(self):
        form.adaptive_line(f'ID {"Title":<30}  {'Author':<15}  {'Year':<6}  {'Stock'}', True)
        book_list = Db.session.query(Db.Book).all()
        for book in book_list:
            if book.stock >=1:
                print(f'{book.id}  {book.title:.<30}  {book.author:<15}  {book.year:<8}  {book.stock}')

    def new_book(self):
        try:
            book_title, author, year, stock = read.new_book()
            new_book = Db.Book(book_title, author, year, stock)
            Db.session.add(new_book)
            Db.session.commit()
        except TypeError as e:
            pass
        else:
            print('New book created in database.')

    def update_stock(self):
        try:
            book_id, stock = read.read_stock()
            book_update = Db.session.query(Db.Book).filter_by(id = book_id).first()
            book_update.stock = stock
            Db.session.commit()
        except TypeError as e:
            pass
        else:
            print('Stock updated sucessfully!')

    def delete_book(self):
        try:
            book_id = read.read_int("Enter a book id:")
            Db.session.delete(book_id)
            Db.session.commit()
        except TypeError as e:
            pass
        else:
            print('Book deleted successfully!')

class UserManager(Db):

    def get_id(self, email):
        user_id = Db.session.query(Db.User).filter_by(email=email).id
        return print(user_id)

    def new_user(self):
        name = input('Enter your name: ')
        email = input('Enter your email: ')
        user = Db.User(name,email)
        Db.session.add(user)
        Db.User.session.commit()

    def register_update(self):
        pass

class LeaseManager(Db):
    def get_id(self):
        pass
    def new_lease(self):
        pass
    def delete_lease(self):
        pass
    @staticmethod
    def lease_time():
        pass