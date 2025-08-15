from common import rental_logic as rl, text_formatter as form

while True:
    form.menu_title('BOOK RENTAL STORE')
    choice = form.menu(['Books available', 'Rent a book', 'Return a book', 'Database management (EMPLOYEES ONLY)', 'Exit'])
    match choice:
        case 'Books available':
            rl.list_to_show('Books')
        case 'Rent a book':
            rl.add_new('leases')
        case 'Return a book':
            rl.return_book()
        case 'Database management (EMPLOYEES ONLY)':
            form.menu_title('Database management')
            choice = form.menu(['Add new', 'Delete data','Update table','Show table', 'Return to main menu'])
            match choice:
                case 'Add new':
                    form.menu_title('ADD OPTIONS')
                    choice = form.menu(['Add new book', 'Add new user', 'Add new lease', 'Return to main menu'])
                    match choice:
                        case 'Add new book':
                            rl.add_new('book')
                        case 'Add new user':
                            rl.add_new('user')
                        case 'Add new lease':
                            rl.add_new('lease')
                        case 'Return to main menu':
                            continue
                case 'Delete data':
                    form.menu_title('DELETE OPTIONS')
                    choice = form.menu(['Delete book', 'Delete user', 'Delete lease', 'Return to main menu'])
                    match choice:
                        case 'Delete book':
                            rl.delete_from_table('Books')
                        case 'Delete user':
                            rl.delete_from_table('Users')
                        case 'Delete lease':
                            rl.delete_from_table('Leases')
                        case 'Return to main menu':
                            continue
                case 'Update table':
                    form.menu_title('UPDATE OPTIONS')
                    choice = form.menu(['Update book', 'Update user', 'Update lease', 'Return to main menu'])
                    match choice:
                        case 'Update book':
                            rl.table_update('Books')
                        case 'Update user':
                            rl.table_update('Users')
                        case 'Update lease':
                            rl.table_update('Leases')
                        case 'Return to main menu':
                            continue
                case 'Show table':
                    form.menu_title('SHOW OPTIONS')
                    choice = form.menu(['Show books', 'Show users', 'Show leases', 'Return to main menu'])
                    match choice:
                        case 'Show books':
                            rl.list_to_show('Books')
                        case 'Show users':
                            rl.list_to_show('Users')
                        case 'Show leases':
                            rl.list_to_show('Leases')
                        case 'Return to main menu':
                            continue
                case 'Return to main menu':
                    continue
                case _:
                    form.adaptive_line('\33[31mERROR! Option not found\33[m')
        case 'Exit':
            break
        case _:
            form.adaptive_line('\33[31mERROR! Option not found\33[m')
form.menu_title('Exiting...')
form.menu_title('Thank you for your preference!')
