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
            book_id = read_int('Book ID: ')
            amount = read_amount()
            customer = input('Customer name: ').strip().title()
            line()
            book_Db.rent_a_book(book_id=book_id, amount = amount, customer = customer)
        case 3:
            book_id = read_int('Book ID: ')
            customer = input('Customer name: ').strip().title()
            book_Db.return_book(book_id = book_id, customer = customer)

        case 4:
            menu_title('STOCK OPTIONS')
            choice = menu(['Add a new book', 'Book stock', 'Remove a book', 'Return to main menu'])
            match choice:
                case 1:
                    new_book_data = new_book()
                    if new_book_data:
                        book_Db.add_new(new_book_data)
                case 2:
                    book_Db.show_list(actual_stock=-100)
                    m, b_id, b_stock = read_stock()
                    book_Db.stock(method=m , book_id=b_id, book_stock=b_stock)
                case 3:
                    book_Db.remove_book(book_id=read_int('Book ID: '))
                case 4:
                    pass
                case _:
                    adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case _:
            adaptive_line('\33[31mERROR! Option not found\33[m')
book_Db.close_conn()
menu_title('Exiting...')
menu_title('Thank you for your preference!')
book_Db.rent_period()
