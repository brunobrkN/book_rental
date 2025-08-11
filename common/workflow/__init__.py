from common import rental_logic as rl, read
def add_new(table):
    match table:
        case 'books':
            rl.add_new_book()
        case 'users':
            rl.add_new_user()
        case 'leases':
            rl.list_to_show('Books')
            rl.add_new_lease()
    return print(f'New {table} registered in database.')

def delete_from_table(table):
    match table:
        case 'books':
            rl.list_to_show('Books')
            book_id = read.read_int("Enter a book id:")
            rl.delete_from_book()
        case 'users':
            rl.list_to_show('Users')
            rl.delete_from_user()
        case 'leases':
            rl.list_to_show('Leases')
            rl.delete_from_lease()

def update_from_table(table):
    match table:
        case 'books':
            pass