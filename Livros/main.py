from common.db_interact import *
while True:
    choice = menu(['Add new book', 'Books available', 'Rent a book', 'Return a book', 'Exit'])
    book_Db = Db()
    if choice == 1:
        book_Db.add_new(data = new_book())
    if choice == 2:
        book_Db.show_list()
    if choice == 3:
        book_Db.show_list()
        line()
        book_Db.rent(id = read_int('Insert a book ID: '))
    if choice == 5 or None:
        break
menu_title('Exiting...')
menu_title('Thank you for your preference!')
book_Db.close_conn()
