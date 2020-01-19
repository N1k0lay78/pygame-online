import socket, time, pickle

host = socket.gethostbyname(socket.gethostname())
print(host)
port = 9090

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

quit = False
print("[ Server Started ]")

while not quit:
    data, addr = s.recvfrom(1024)

    if addr not in clients:
        clients.append(addr)

    itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
    # dataform = str(data).strip("'<>() ").replace('\'', '\"')
    struct = pickle.loads(data)
    print(struct)
    for client in clients:
        if addr != client:
            # print('re')
            s.sendto(data, client)

print("\n[ Server Stopped ]")
quit = True

s.close()