from common.db_interaction import *
while True:
    menu_title('BOOK RENTAL STORE')
    choice = menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    book_Db = Db()
    match choice:
        case 1:
            book_Db.show_list()
        case 2:
            book_Db.show_list()
            line()
            book_Db.rent_a_book(book_id=read_int('Book ID: '))
        case 3:
            book_Db.return_book(book_id = read_int('Book ID: '))
        case 4:
            menu_title('STOCK OPTIONS')
            choice = menu(['Add a new book', 'Book stock', 'Remove a book', 'Return to main menu'])
            match choice:
                case 1:
                    new_book_data = new_book()
                    if new_book_data:
                        book_Db.add_new(new_book_data)
                case 2:
                    m, b_id, b_stock = read_stock()
                    book_Db.stock(method=m , book_id=b_id, book_stock=b_stock)
                case 3:
                    book_Db.remove_book(book_id=read_int('Book ID: '))
                case 4:
                    pass
        case 5:
            break
book_Db.close_conn()
menu_title('Exiting...')
menu_title('Thank you for your preference!')
