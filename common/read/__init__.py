from common import text_formatter, rental_logic as rl
def new_book():
    """
        → Lê os dados necessários para a função add_book().
    :return: Lista com todos os dados lidos.
    """
    book_title = input('Book name: ').strip()
    author = input('Author: ').title().strip()
    year = read_int('Publication year: ')
    stock = read_int('Stock: ')
    text_formatter.adaptive_line('Adding new book, please confirm the data.', True)
    if confirm() == 'Y':
        return book_title,author,year,stock
    else:
        return None

def read_stock():
    """
        → Lê os dados necessários para função stock().
    :return: Lista com todos os dados lidos
    """
    book_id = read_int('Book ID: ')
    book_stock = read_int('New book stock: ')
    return  book_id, book_stock

def read_int(msg):
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
    """
        → Lê repostas de confirmação (Y/N).
    :param msg: Mensagem a ser exibida para o usuário.
    :return: Resposta 'Y' ou 'N'
    """
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

def read_new_lease( ):
    answer = confirm(msg='Do you already have a store registration?(Y/N): ')
    if answer == 'Y':
        pass
    if answer == 'N':
        rl.add_new('user')
    book_id = read_int('Book ID: ')
    amount = read_int('How many books do you want to rent?: ')
    email = input('Email: ').lower().strip()
    return email,amount,book_id

def read_menu_choice():
    choice = read_int('Select an option: ')
    return choice
