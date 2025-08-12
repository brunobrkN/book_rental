from common import rental_logic as rl, text_formatter as form

while True:
    form.menu_title('BOOK RENTAL STORE')
    choice = form.menu(['Books available', 'Rent a book', 'Return a book', 'Stock (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 1:
            rl.list_to_show('Books')
        case 2:
            rl.add_new('leases')
        case 3:
            rl.return_book()
        case 4:
            form.menu_title('STOCK OPTIONS')
            choice = form.menu(['Add new', 'Delete data','Update table', 'Return to main menu'])
            match choice:
                case 1:
                    form.menu_title('ADD OPTIONS')
                    choice = form.menu(['Add new book', 'Add new user', 'Add new lease', 'Return to main menu'])
                    match choice:
                        case 1:
                            rl.add_new('book')
                        case 2:
                            rl.add_new('user')
                        case 3:
                            rl.add_new('lease')
                        case 4:
                            continue
                case 2:
                    form.menu_title('DELETE OPTIONS')
                    choice = form.menu(['Delete book', 'Delete user', 'Delete lease', 'Return to main menu'])
                    match choice:
                        case 1:
                            rl.delete_from_table('Books')
                        case 2:
                            rl.delete_from_table('Users')
                        case 3:
                            rl.delete_from_table('Leases')
                        case 4:
                            continue
                case 3:
                    form.menu_title('UPDATE OPTIONS')
                    choice = form.menu(['Update book', 'Update user', 'Update lease', 'Return to main menu'])
                    match choice:
                        case 1:
                            rl.table_update('Books')
                        case 2:
                            rl.table_update('Users')
                        case 3:
                            rl.table_update('Leases')
                        case 4:
                            continue
                case 4:
                    continue
                case _:
                    form.adaptive_line('\33[31mERROR! Option not found\33[m')
        case 5:
            break
        case _:
            form.adaptive_line('\33[31mERROR! Option not found\33[m')
form.menu_title('Exiting...')
form.menu_title('Thank you for your preference!')
