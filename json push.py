import socket, threading, time
from pickle import dumps
import pickle

key = 8194

shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                # print(data.decode("utf-8"))
                struct = pickle.loads(data)
                print(struct)
                # Begin
                print('cds')
                # End

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
        slow = {'gg': 'hello'}
        print("push")
        s.sendto(dumps(slow), server)
        time.sleep(0.2)

rT.join()
s.close()