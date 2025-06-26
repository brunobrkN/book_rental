from common.db_interact import *
while True:
    menu_title('BOOK RENTAL STORE')
    choice = menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    book_Db = Db()
    if choice == 1:
        book_Db.show_list()
    if choice == 2:
        book_Db.show_list()
        line()
        book_Db.rent(book_id=read_int('Book ID: '))
    if choice == 4:
        menu_title('STOCK OPTIONS')
        choice = menu(['Add a new book', 'Book stock', 'Return to main menu'])
        if choice == 1:
            book_Db.add_new(data = new_book())
        if choice == 2:
            m, b_id, b_stock = read_stock()
            book_Db.stock(method=m , book_id=b_id, book_stock=b_stock)
    if choice == 5 or None:
        break
book_Db.close_conn()
menu_title('Exiting...')
menu_title('Thank you for your preference!')
