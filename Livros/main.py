from common.db_interact import *
while True:
    choice = menu(['Add new book', 'Books available', 'Rental new book', 'Return a book', 'Exit'])
    book = Db()
    rent = Db()
    if choice == 1:
        book.add_new(data = new_book())
    if choice == 2:
        book.show_list()
    if choice == 3:
        book.show_list()
        line()
        rent.rental(id = read_int('Choose an ID and insert to rental: '))
    if choice == 5 or None:
        break
menu_title('Exiting...')
menu_title('Thank you for your preference!')
