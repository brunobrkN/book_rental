from common.read import *
def line(x=60):
    return print('-' * x)

def menu_title(msg):
    """
    → Formatação padrão das funções principais do sistema.
    :param msg: Função a ser exibida
    :return:
    """
    line()
    print(msg.center(50))
    line()


def menu(list):
    """
    → Lista para o usuário as opções disponíveis no menu
    :param list: Todas as opções possíveis (pode ser adicionado diretamente no código principal)
    :return:
    """
    menu_title('BOOK RENTAL STORE')
    count = 1
    for i in list:
        print(f'\33[36m{count}-\33[34m {i}\33[m')
        count += 1
    option = read_int('\33[33mChoose an option: \33[m')
    return option



