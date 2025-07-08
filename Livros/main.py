from common.db_interaction import *
from common import rental_logic as rl
while True:

    menu_title('BOOK RENTAL STORE')
    choice = menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 1:
            rl.book_db.show_list()
        case 2:
            rl.book_db.show_list()
            book_id = read_int('Book ID: ')
            rl.rent_a_book(book_id=book_id)
        case 3:
            rental_id = read_int('Rental ID: ')
            book_id = read_int('Book ID: ')
            rl.return_book(rental_id = rental_id, book_id = book_id)

        case 4:
            menu_title('STOCK OPTIONS')
            choice = menu(['Add a new book', 'Book stock', 'Remove a book', 'Return to main menu'])
            match choice:
                case 1:
                    new_book_data = new_book()
                    if new_book_data:
                        rl.book_db.insert(new_book_data)
                case 2:
                    rl.book_db.show_list(actual_stock=-100)
                    m, b_id, b_stock = read_stock()
                    rl.book_db.stock_update(method=m, book_id=b_id, book_stock=b_stock)
                case 3:
                    rl.book_db.remove(id=read_int('Book ID: '))
                case 4:
                    pass
                case _:
                    adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case 6:
            ID = read_int('Book ID: ')
            rl.book_db.id_exists(ID)
        case _:
            adaptive_line('\33[31mERROR! Option not found\33[m')
rl.book_db.close_conn()
menu_title('Exiting...')
menu_title('Thank you for your preference!')
