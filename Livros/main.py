from common import rental_logic as rl, text_formatter as form, read
while True:
    form.menu_title('BOOK RENTAL STORE')
    choice = form.menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 1:
            rl.book_db.show_list()
        case 2:
            rl.book_db.show_list()
            book_id = read.read_int('Book ID: ')
            rl.rent_a_book(book_id=book_id)
        case 3:
            rental_id = read.read_int('Rental ID: ')
            book_id = read.read_int('Book ID: ')
            rl.return_book(rental_id = rental_id, book_id = book_id)

        case 4:
            form.menu_title('STOCK OPTIONS')
            choice = form.menu(['Add a new book', 'Book stock', 'Remove a book', 'Return to main menu'])
            match choice:
                case 1:
                    new_book_data = read.new_book()
                    if new_book_data:
                        rl.book_db.insert(new_book_data)
                case 2:
                    rl.book_db.show_list(actual_stock=-100)
                    m, b_id, b_stock = read.read_stock()
                    rl.book_db.stock_update(method=m, book_id=b_id, book_stock=b_stock)
                case 3:
                    rl.book_db.remove(id=read.read_int('Book ID: '))
                case 4:
                    pass
                case _:
                    form.adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case _:
            form.adaptive_line('\33[31mERROR! Option not found\33[m')
rl.book_db.close_conn()
form.menu_title('Exiting...')
form.menu_title('Thank you for your preference!')
