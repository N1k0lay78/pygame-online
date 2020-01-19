import pygame
from win32api import GetSystemMetrics
import socket, threading, time
from pickle import dumps
import pickle


class Person:
    def __init__(self, pos, r, name, color):
        # данные о персонаже
        self.data = {'pos': pos, 'r': r, 'name': name, 'type': 'Player', 'color': pygame.Color(color)}

    def get_json(self):
        # получить словарь для отправки на сервер и с сервера игрокам
        return self.data

    def update(self, data):
        # обновление координат персонажа
        l, r, u, down = data
        # предыдущие координаты для проверки
        last_pos = self.data['pos'][:]
        if l:
            self.data['pos'][0] -= speed
        if r:
            self.data['pos'][0] += speed
        if u:
            self.data['pos'][1] -= speed
        if down:
            self.data['pos'][1] += speed
        # если координаты изменились, то добовляем персонажа в список изменившихся объектов d
        if last_pos != self.data['pos']:
            global d
            d['objects'].append(self.data)


class ObjectGroup:
    def __init__(self, name, ip_server, color):
        # окно размером с весь экран
        size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
        # небольшое окно если так удобнее
        size_screen = (300, 300)
        self.screen = pygame.display.set_mode(size_screen)
        # объекты этого игрока (которые надо обнолять)
        self.objects1 = [Person([100, 100], 10, name, color)]
        pygame.display.flip()
        global objects
        global d
        # игрок никуда не идёт
        self.motions = [False, False, False, False]
        # добовляем в список объектов
        objects['objects'].append(self.objects1[0].get_json())
        # добовляем в вписок обновлений
        d['objects'].append(self.objects1[0].get_json())

    def push(self, info):
        # пушим обновления info - информация которая изменилась
        global s, d
        # показывем что отправляем
        print('push', d)
        # отпровляем изменения
        s.sendto(dumps(d), server)

    def update(self):
        global d, objects
        # обробатывем события
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
        # обробатываем ГГ
        self.objects1[0].update(self.motions)
        # если есть изменения отправляем их на сервер
        if d != {'objects': [], 'online': []}:
            self.push(d)
            # делаем список изменений пустым
            d = {'objects': [], 'online': []}
        # отрисовываем
        for values in objects.values():
            for object in values:
                object = object
                if object['type'] == 'Player':
                    pygame.draw.circle(self.screen, object['color'], object['pos'], object['r'])
        pygame.display.flip()


key = 8194

shutdown = False
join = False

# если интересно как работает смотрите:
# https://www.youtube.com/watch?v=MPjgHxK8k68
# т. к. это его доработаный код
def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                # загружаем обновления
                struct = pickle.loads(data)
                global objects
                for key in struct:
                    objects[key].extend(struct[key])

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = [None, 9090]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

# данные игрока
alias = input("Name: ")
server[0] = input('server IP: ')
color = input('color: ')
server = tuple(server)
# скорость
speed = 5
# список json объектов
objects = {'objects': [], 'online': []}
# список изменившихся json объектов (который мы отправляем на сервер)
d = {'objects': [], 'online': []}
# создаём игру
game = ObjectGroup(alias, server, color)

# многопоточность
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# игровой цикл
while not shutdown:
    if join == False:
        join = True
    else:
        # обносляем игру и если есть изменения, то она отправит изменения
        game.update()
        # ограничение FPM ))
        time.sleep(0.2)

# выключаем поток
rT.join()
s.close()
