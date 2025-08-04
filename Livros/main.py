from common import rental_logic as rl, text_formatter as form, read
from common.db_interaction import DbInteraction


books = rl.BookManager()


while True:
    form.menu_title('BOOK RENTAL STORE')
    choice = form.menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 1:
            books.show_list()
        case 2:
            books.show_list()
            books.new_book()
        case 3:
            rental_id = read.read_int('Rental ID: ')
            book_id = read.read_int('Book ID: ')
            rl.return_book(rental_id = rental_id, book_id = book_id)

        case 4:
            form.menu_title('STOCK OPTIONS')
            choice = form.menu(['Add a new book', 'Book stock', 'Remove a book', 'Return to main menu'])
            match choice:
                case 1:
                    books.new_book()
                case 2:
                    books.update_stock()
                case 3:
                    pass
                case 4:
                    pass
                case _:
                    form.adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case _:
            form.adaptive_line('\33[31mERROR! Option not found\33[m')

form.menu_title('Exiting...')
form.menu_title('Thank you for your preference!')
