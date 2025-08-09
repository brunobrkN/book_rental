from common import rental_logic as rl, text_formatter as form, read, workflow


while True:
    form.menu_title('BOOK RENTAL STORE')
    choice = form.menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 1:
            rl.show_books()
        case 2:
            rl.show_books()
            workflow.add_new('leases')
        case 3:
            rl.return_book()
        case 4:
            form.menu_title('STOCK OPTIONS')
            choice = form.menu(['Add a new book', 'Book stock', 'Remove a book', 'Delete user', 'Delete rental', 'Return to main menu'])
            match choice:
                case 1:
                    workflow.add_new('books')
                case 2:
                    rl.show_books()
                    book_id, stock = read.read_stock()
                    rl.stock_update(book_id, stock)
                case 3:
                    rl.show_books()
                    book_id = read.read_int("Enter a book id:")
                    workflow.delete_from_table('books')
                case 4:
                    rl.show_users()
                    workflow.delete_from_table('users')
                case 5:
                    rl.show_leases()
                    workflow.delete_from_table('leases')
                case 6:
                    continue
                case _:
                    form.adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case _:
            form.adaptive_line('\33[31mERROR! Option not found\33[m')

form.menu_title('Exiting...')
form.menu_title('Thank you for your preference!')
