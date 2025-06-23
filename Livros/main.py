#Locadora de livros, com funções de verificar livros disponíveis, emprestar/devolver livros, adicionar novos livros e verificar para quem foi emprestado e prazo restante para devolução.
#Objetivos: Praticar POO, manipulação de arquivos e outros conceitos básicos de programação. (Sei que seria melhor fazer usando banco de dados)
from common.db_interact import *
while True:
    choice = menu(['Add new book', 'Books available', 'Rental new book', 'Return a book', 'Exit'])
    book = Db()
    if choice == 1:
        book.add_new(data = new_book())
    if choice == 5 or None:
        break
menu_title('Exiting...')
menu_title('Thank you for your preference!')
