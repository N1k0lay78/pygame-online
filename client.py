import pygame
from win32api import GetSystemMetrics
import socket, threading, time
from pickle import dumps
import pickle


class Person:
    def __init__(self, pos, r, name, color):
        self.data = {'pos': pos, 'r': r, 'name': name, 'type': 'Player', 'color': pygame.Color(color)}

    def get_json(self):
        return self.data

    def update(self, data):
        l, r, u, down = data
        last_pos = self.data['pos'][:]
        if l:
            self.data['pos'][0] -= speed
        if r:
            self.data['pos'][0] += speed
        if u:
            self.data['pos'][1] -= speed
        if down:
            self.data['pos'][1] += speed
        if last_pos != self.data['pos']:
            global d
            d['objects'].append(self.data)


class ObjectGroup:
    def __init__(self, name, ip_server, color):
        size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
        size_screen = (300, 300)
        self.screen = pygame.display.set_mode(size_screen)
        self.objects1 = [Person([100, 100], 10, name, color)]
        pygame.display.flip()
        global objects
        global d
        self.motions = [False, False, False, False]
        objects['objects'].append(self.objects1[0].get_json())
        d['objects'].append(self.objects1[0].get_json())

    def push(self, info):
        # пушим обновления info - информация которая изменилась
        global s, d
        print('push', d)
        s.sendto(dumps(d), server)

    def add_objects(self, object):
        self.objects['objects'].append(object)
        self.d['object'].append(object)

    def update(self):
        global d, objects
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global shutdown
                shutdown = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.motions[0] = True
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.motions[1] = True
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.motions[2] = True
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.motions[3] = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.motions[0] = False
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.motions[1] = False
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.motions[2] = False
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.motions[3] = False
        self.objects1[0].update(self.motions)
        if d != {'objects': [], 'online': []}:
            self.push(d)
            d = {'objects': [], 'online': []}
        for values in objects.values():
            for object in values:
                object = object
                if object['type'] == 'Player':
                    pygame.draw.circle(self.screen, object['color'], object['pos'], object['r'])
        pygame.display.flip()


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
                global objects
                for key in struct:
                    objects[key].extend(struct[key])
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
color = input('color: ')
server = tuple(server)
speed = 5
objects = {'objects': [], 'online': []}
d = {'objects': [], 'online': []}
game = ObjectGroup(alias, server, color)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while not shutdown:
    if join == False:
        join = True
    else:
        game.update()
        time.sleep(0.2)

rT.join()
s.close()
