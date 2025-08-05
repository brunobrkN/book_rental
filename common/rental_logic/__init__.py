from common import text_formatter as form, read
from common.db_interaction import DbInteraction as Db

def show_list():
    form.adaptive_line(f'ID {"Title":<30}  {'Author':<15}  {'Year':<10}  {'Stock'}', True)
    book_list = Db.session.query(Db.Book).all()
    for book in book_list:
        if book.stock >=1:
            print(f'{book.id}  {book.title:.<30}  {book.author:<15}  {book.year:<10}  {book.stock}')

def add_new(table):
    match table:
        case 'book':
            try:
                book_title, author, year, stock = read.new_book()
                new_book = Db.Book(book_title, author, year, stock)
                Db.session.add(new_book)
                Db.session.commit()
            except Exception as e:
                print('ERROR:', e)
        case 'user':
            name = input('Name: ').strip().title()
            email = input('Email: ').strip().lower()
            email_query = Db.session.query(Db.User).filter_by(email=email).all()
            if email_query:
                if email_query.email:
                        return print('Email already registered')
                else:
                    new_user = Db.User(name,email)
                    Db.session.add(new_user)
                    Db.session.commit()
            else:
                new_user = Db.User(name,email)
                Db.session.add(new_user)
                Db.session.commit()

        case 'lease':
            email, amount,book_id = read.read_new_lease()
            return_date,acquisition = lease_time()
            owner_id = Db.session.query(Db.User).filter_by(email=email).first()
            lease_data = Db.Leased(owner_id=owner_id.id, book_id=book_id, amount = amount, acquisition=acquisition, return_date=return_date)
            Db.session.add(lease_data)
            book_update = Db.session.query(Db.Book).filter_by(id=book_id).first()
            book_update.stock = book_update.stock - amount
            Db.session.commit()
    return print(f'New {table} registered in database.')

def stock_update(book_id, stock):
    try:
        book_update = Db.session.query(Db.Book).filter_by(id = book_id).first()
        book_update.stock = stock
        Db.session.commit()
    except TypeError as e:
        pass
    else:
        print('Stock updated sucessfully!')

def delete_from_table(table,id):
    match table:
        case 'book':
            try:
                id_query = Db.session.query(Db.Book).filter_by(id=id).first()
                Db.session.delete(id_query)
                Db.session.commit()
            except TypeError as e:
                print(f'ERROR {e}! Book not found.')
            else:
                print('Book deleted successfully!')
        case 'lease':
            id_query = Db.session.query(Db.Leased).filter_by(rental_id=id).first()
            Db.session.delete(id_query)
            Db.session.commit()

def return_book():
    try:
        email = input('Email: ').strip().lower()
        user_query = Db.session.query(Db.User).filter_by(email=email).first()
        lease_query = Db.session.query(Db.Leased).filter_by(owner_id=user_query.id).all()
        form.adaptive_line(f'{'Rental ID':10} {'Owner ID':10} {'Book ID':10} {'Amount':10} {'Acquisition':14}{'Return Date':10}',True)
        for lease in lease_query:
            print(f'{lease.rental_id:<10} {lease.owner_id:<10} {lease.book_id:<10} {lease.amount:<10}  {lease.acquisition:<14} {lease.return_date:<10}')
    except AttributeError as e:
        print(f'ERROR {e}! Email not found.')
    else:
        rental_id = read.read_int('Select a rental ID to return: ')
        id_query = Db.session.query(Db.Leased).filter_by(rental_id=rental_id).first()
        update_stock = Db.session.query(Db.Book).filter_by(id=id_query.book_id).first()
        print(update_stock)
        new_stock = update_stock.stock + id_query.amount
        stock_update(update_stock.id, new_stock)
        delete_from_table('lease', rental_id)

def lease_time():
    from datetime import datetime, timedelta
    today = datetime.today().date()
    return_date = today + timedelta(days = 7)
    return return_date,today
