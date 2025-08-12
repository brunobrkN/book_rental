from common import text_formatter as form, read
from common.db_interaction import DbInteraction as Db

def add_new(table):
    match table:
        case 'book':
            add_new_book()
        case 'user':
            add_new_user()
        case 'leases':
            list_to_show('Books')
            add_new_lease()
    return print(f'New {table} registered in database.')

def add_new_book():
    try:
        book_title, author, year, stock = read.new_book()
        new_book = Db.Books(book_title, author, year, stock)
        Db.session.add(new_book)
        Db.session.commit()
    except Exception as e:
        print(f'\33[31mERROR to add new book:{e}\33[m')

def add_new_user():
    name = input('Name: ').strip().title()
    email = input('Email: ').strip().lower()
    email_query = Db.session.query(Db.Users).filter_by(email=email).first()
    if email_query:
        return print('Email already registered')
    else:
        new_user = Db.Users(name, email)
        Db.session.add(new_user)
        Db.session.commit()

def  add_new_lease():
    email, amount,book_id = read.read_new_lease()
    return_date,acquisition = lease_time()
    owner_id = Db.session.query(Db.Users).filter_by(email=email).first()
    if not owner_id:
        return print('Email not registered.')
    lease_data = Db.Leases(owner_id=owner_id.id, book_id=book_id, amount = amount, acquisition=acquisition, return_date=return_date, status='Active')
    Db.session.add(lease_data)
    book_update = Db.session.query(Db.Books).filter_by(id=book_id).first()
    book_update.stock = book_update.stock - amount
    Db.session.commit()

def delete_from_table(table):
    list_to_show(table)
    query = int(input('Id to delete: '))
    delete_data = Db.session.query(getattr(Db,table)).filter_by(id=query).first()
    if delete_data:
        Db.session.delete(delete_data)
        Db.session.commit()
        print('User deleted!')

def lease_time():
    from datetime import datetime, timedelta
    today = datetime.today().date()
    return_date = today + timedelta(days = 7)
    return return_date,today

def return_book():
    try:
        email = input('Email: ').strip().lower()
        user_query = Db.session.query(Db.Users).filter_by(email=email).first()

        if not user_query:
            return print('User does not exist!')
        lease_query = Db.session.query(Db.Leases).filter_by(owner_id=user_query.id).all()

        if not lease_query:
            return print('User not have a leased books!')

        form.adaptive_line(f'{'Rental ID':10} {'Owner ID':10} {'Book ID':10} {'Amount':10} {'Acquisition':14}{'Return Date':10} {"Status"}',True)
        count = 0
        for lease in lease_query:
            if lease.status == 'Active':
                print(f'{lease.id:<10} {lease.owner_id:<10} {lease.book_id:<10} {lease.amount:<10}  {lease.acquisition:<14} {lease.return_date:<10} {lease.status:<10}')
                count += 1
        if count == 0:
            return print('No leases available to this user!')
        rental_id = read.read_int('Select a rental ID to return: ')
        id_query = Db.session.query(Db.Leases).filter_by(id=rental_id).first()

        if not id_query:
            return print('Rental ID not found!')

        if not id_query.status:
            return print('Rental ID is already inactive!')

        update_stock = Db.session.query(Db.Books).filter_by(id=id_query.book_id).first()
        if not update_stock:
            return print('Book ID not found!')

        new_stock = update_stock.stock + id_query.amount
        stock_update(update_stock.id, new_stock)
        id_query.status = 'Inactive'
        Db.session.commit()
    except Exception as e:
        print(f'\33[31mError returning book: {e}\33[m')

def show_list(table_class, columns):
    table_lists =  Db.session.query(table_class).all()
    for item in table_lists:
        data_string = ' '.join([f'{getattr(item, field):<{width}}' for field, width in columns.items()])
        print(data_string)

def list_to_show(table):
    table_class = getattr(Db, table)
    columns = Db.Books.metadata.tables[table].columns.keys()
    if table == 'Leases':
        width = [9,8,7,6,11,11,8]
    else:
        width = [4,25,15,4,4]
    columns_dict = dict(zip(columns, width))
    header = ' '.join(f'{column.title():<{width}}' for column, width in columns_dict.items()).replace('_', ' ')
    form.adaptive_line(header, True)
    show_list(table_class, columns_dict)

def stock_update(book_id, stock):
    try:
        book_update = Db.session.query(Db.Books).filter_by(id = book_id).first()
        if book_update:
            book_update.stock = stock
            Db.session.commit()
            print('Stock updated sucessfully!')
    except Exception as e:
        print(f'\33[31mERROR to update book:{e}')

def table_update(table):
    try:
        list_to_show(table)
        id_to_update = read.read_int('Select a ID to update: ')
        columns = Db.Books.metadata.tables[table].columns.keys()
        column = columns[int(form.menu(columns)-1)]
        table_class = getattr(Db, table)
        update = Db.session.query(table_class).filter_by(id = id_to_update).first()
        if not update:
            print('ID not found!')
        new_data = input('Enter new data: ')
        setattr(update, column, new_data)
        Db.session.commit()
        print(f'{column} data updated sucessfully!')
    except Exception as e:
        print(f'\33[31mERROR to update table:{e}')
