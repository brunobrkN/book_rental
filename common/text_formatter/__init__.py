from common import read
def line(length=65):
    print('-' * length)

def adaptive_line( phrase, second_line = False):
    line(len(phrase.replace('\33[31m', '').replace('\33[m', '')))
    print(phrase)
    if second_line:
        line(len(phrase))

def menu_title(msg):
    """
    → Formatação padrão das funções principais do sistema.
    :param msg: Função a ser exibida
    :return:
    """
    line()
    print(msg.center(60))
    line()

def menu(options):
    """
    → Lista para o usuário as opções disponíveis no menu
    :param options: Todas as opções possíveis (pode ser adicionado diretamente no código principal)
    :return:
    """
    count = 1
    for i in options:
        print(f'\33[36m{count}-\33[34m {i}\33[m')

        count += 1
    choice = read.read_int('Select an option: ')
    return options[choice - 1]
