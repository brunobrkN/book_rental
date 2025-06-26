from common import interface
def new_book():
    book_name = input('Book name: ').title().strip()
    author = input('Author: ').title().strip()
    year = read_int('Publication year: ')
    stock = read_int('Stock: ')
    interface.menu_title('Adding new book, please confirm the data.')
    if confirm() == 'Y':
        return book_name,author,year,stock
    else:
        return None

def read_stock():
    book_id = input('Book ID: ')
    book_stock = read_int('Amount: ')
    print('1- Add to current stock')
    print('2- Replace current stock')
    method = read_int('Choose an option: ')
    return method, book_id, book_stock


def read_int(msg): #precisa ser revisto para as escolhas não ultrapassarem o valor limite em menu_title
    """
    => Lê um número inteiro previnindo possíveis erros de digitação/interrupção do programa.
    :param msg: Script exibido para o usuário
    :return: Valor inteiro informado pelo usuário
    """
    while True:
        try:
            valor = int(input(msg))
            return valor
        except KeyboardInterrupt:
            print('\n\33[31mUser interrupted the application.\33[m')
            return None
        except (ValueError, TypeError):
            print('\33[31mERROR! Value is not numeric.\33[m')

def confirm(msg = 'Do you want to continue?(Y/N): '):
    while True:
        try:
            answer = input(msg).strip().upper()[0]
            if answer in 'YN':
                return answer
            else:
                print('\33[31mERROR! Please insert Y or N.\33[m')
        except KeyboardInterrupt:
                print('\n\33[31mUser interrupted the application.\33[m')
        except IndexError:
            print('\33[31mERROR! Please insert Y or N.\33[m')
