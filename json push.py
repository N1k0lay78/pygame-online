import socket, threading, time
from pickle import dumps
import pickle

# если хочешь понять как работает
# https://www.youtube.com/watch?v=MPjgHxK8k68
key = 8194

shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                # принимаем данные
                data, addr = sock.recvfrom(1024)
                # расшифровываем и выводим
                struct = pickle.loads(data)
                print(struct)
                time.sleep(0.2)
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = 0

server = [None, 9090]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Name: ")
server[0] = input('server IP: ')
server = tuple(server)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:
        join = True
    else:
        message = input()
        # если что то ввели то создаём словарь с данными
        slow = {'gg': 'hello'}
        print("push")
        # и отправляем их
        s.sendto(dumps(slow), server)
        time.sleep(0.2)

rT.join()
s.close()