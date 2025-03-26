import threading
from time import sleep
from threading import Thread

def requisicao():
        print("Fazendo requisicao web ...")
        sleep(3)
        print("Fim")


t1 = Thread(target=requisicao)
t1.start()

t2 = Thread(target=requisicao)
t2.start()

t3 = Thread(target=requisicao)
t3.start()