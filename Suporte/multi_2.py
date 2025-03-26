from time import sleep
from threading import Thread

lista = []
def requisicao():

        cont = "*"
        lista.append(cont)
        print(*lista)

global t
lista_threads = []

# Lista de Threads
for i in range(100):
    t = Thread(target=requisicao)
    lista_threads.append(t)

for i in lista_threads:
    i.start()

for i in lista_threads:
    i.join()