import socket, time, pickle

host = socket.gethostbyname(socket.gethostname())
# выводим host к которому подключаются игроки
print(host)
# порт
# если хочешь понять как работает
# https://www.youtube.com/watch?v=MPjgHxK8k68
#
port = 9090

clients = []

# хз что это но лучше не трогать
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

quit = False
# выводим сообщение что сервер готтов
print("[ Server Started ]")

while not quit:
    # получаем данные
    data, addr = s.recvfrom(1024)

    # если игрок не на сервере
    if addr not in clients:
        clients.append(addr)

    # время сейчас не используется
    itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
    # расшифровываем и выводим данные
    struct = pickle.loads(data)
    print(struct)
    # рассылаем данные игрокам кроме того который прислал
    for client in clients:
        if addr != client:
            # print('re')
            s.sendto(data, client)

# выключаем ссервер
print("\n[ Server Stopped ]")
quit = True

s.close()