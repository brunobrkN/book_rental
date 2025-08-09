from common import rental_logic as rl
def add_new(table):
    match table:
        case 'books':
            rl.add_new_book()
        case 'users':
            rl.add_new_user()
        case 'leases':
            rl.add_new_lease()
    return print(f'New {table} registered in database.')

def delete_from_table(table):
    match table:
        case 'books':
            rl.delete_from_book()
        case 'users':
            rl.delete_from_user()
        case 'leases':
            rl.delete_from_lease()

def update_from_table(table):
    match table:
        case 'books':
            pass