import pygame
from random import randint

pygame.init()
size = 1000
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption('Star Fight')

# Ниже константы
WIDTH = 128  # Длина корабля     Я изначально сделал игру без спрайтов, просто с картинками, но потом понял,
HEIGHT = 128  # Ширина корабля   что мне нужны столкновения, переделал, и остались некоторые такие вещи, связанные с
#                                изначальным отсутствием спрайтов
LASER_COUNT = 2  # Максимальное кол-во снарядов на карте
ENEMY_RELOAD = 30  # На число можно не обращать внимания, я делал таймер, и, если честно, не понял, зачем нужно число
#                    в данной переменной

score = 0  # Счет в игре
lifes = 4  # Жизни. Нужны, чтобы игрок не мог просто пропускать мимо себя противников
reloading = False  # Перезарядка. В основном цикле будет пояснение, зачем она нужна
freeze = False  # Пытался реализовать паузу, о ней тоже в цикле


fone_image = pygame.image.load('images/fone.jpg')  # Загружка изображения фона
#                                                    Можно было запихать все вышеперечисленные переменные в класс,
#                                                    но я не до конца понял, какой должен быть этот класс

fps = 120  # Кадры в секунду


class Enemy(pygame.sprite.Sprite):  # Класс противников
    def __init__(self, enemy_x):
        super().__init__()
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = enemy_x
        self.rect.y = 1000
        self.enemy_speed = 8

    def update(self):  # Движение противников в функции update
        self.rect.y -= self.enemy_speed


class Laser(pygame.sprite.Sprite):  # Класс снаряда
    def __init__(self, laser_x):
        super().__init__()
        self.image = pygame.image.load('images/laser.png')
        self.rect = self.image.get_rect()
        self.rect.x = laser_x
        self.rect.y = 238
        self.laser_speed = 30

    def update(self):  # Движение снаряда в функции update
        self.rect.y += self.laser_speed


class Player(pygame.sprite.Sprite):  # Класс игрока
    def __init__(self, player_x):
        super().__init__()
        self.right = False
        self.left = False
        self.image = pygame.image.load('images/spaceship.png')  # Пытался реализовать наклон корабля во время движения.
        self.rect = self.image.get_rect()  # .                    В папке есть картинки с кораблем, наклоненным
        self.rect.x = player_x  # .                               вправо и влево.
        self.rect.y = 100
        self.player_speed = 15

    def update(self):
        pass


class BorderUp(pygame.sprite.Sprite):  # Класс, создающий верхнюю границу, чтобы при столкновении с ней противники
    def __init__(self, x1, y1, x2, y2):  # отнимали жизнь и удалялись из группы спрайтов противников.
        super().__init__()
        self.add(horizontal_border_up)
        self.image = pygame.Surface([x2 - x1, 1])
        self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class BorderDown(pygame.sprite.Sprite):  # Класс, создающий нижнюю границу, чтобы при столкновении с ней снаряды
    def __init__(self, x1, y1, x2, y2):  # удалялись из группы спрайтов снарядов.
        super().__init__()
        self.add(horizontal_border_down)
        self.image = pygame.Surface([x2 - x1, 1])
        self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def draw():
    screen.blit(fone_image, (-480, -480))  # Функция, отрисовывающая все объекты.
    enemies_sprites.update()  # .            Она также обновляет положение объектов, а также
    lasers_sprites.update()  # .             отображает счёт и количество жизней.
    enemies_sprites.draw(screen)
    lasers_sprites.draw(screen)
    spaceships.draw(screen)
    write_score()
    write_lifes()
    pygame.display.flip()


def pause():
    Player.player_speed = 0  # Пытался реализовать пазу при нажатии на ESC, просто занижая скорость всех объектов.
    Laser.laser_speed = 0
    Enemy.enemy_speed = 0


def prodolzhit():
    Player.player_speed = 15  # Функция, которая должна была продолжать игру после паузы.
    Enemy.enemy_speed = 8
    Laser.laser_speed = 30


def write_score():  # Функция, которая создает надпись со счётом.
    font = pygame.font.Font(None, 50)
    text = font.render(f"Score: {score}", 1, (255, 255, 255))
    text_x = 800
    text_y = 50
    screen.blit(text, (text_x, text_y))


def write_lifes():  # Функция, которая создает надпись с количеством жизней.
    font = pygame.font.Font(None, 50)
    text = font.render(f"Lifes: {lifes}", 1, (255, 255, 255))
    text_x = 100
    text_y = 50
    screen.blit(text, (text_x, text_y))


enemies_sprites = pygame.sprite.Group()
lasers_sprites = pygame.sprite.Group()  # Группы всех спрайтов.
spaceships = pygame.sprite.Group()  # Включил спрайт игрока в группу, т.к. не понял, как рисовать спрайт отдельно.

horizontal_border_up = pygame.sprite.Group()  # Создание группы верхней границы и экземпляра верхней границы.
BorderUp(0, 0, 1000, 0)

horizontal_border_down = pygame.sprite.Group()  # Создание группы нижней границы и экземпляра нижней границы.
BorderDown(0, 1000, 1000, 1000)


spaceship = Player(1000 / 2 - 64)  # Создание группы игрока и экземпляра самого игрока.
spaceships.add(spaceship)

clock = pygame.time.Clock()  # Отсчёт кол-ва миллисекунд для задержки отрисовки.

run = True  # Начало игрового цикла

pygame.time.set_timer(ENEMY_RELOAD, 670)  # Таймер для отсчёта времени, после окончания которого появляется противник.

while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not freeze:
                freeze = True
            else:
                freeze = not freeze  # Попытка реализовать паузу
                prodolzhit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # В данном случае использовал reload
            if len(lasers_sprites) < LASER_COUNT and not reloading:  # из-за того, что при нажати на пробел
                lasers_sprites.add(Laser(spaceship.rect.x + 60))  # могло выходить несколько снарядов,
                reloading = True  # .                   а мне нужно было, чтобы при нажатии вылетал один снаряд.
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            reloading = False

        if event.type == ENEMY_RELOAD:  # При срабатывании таймера в группу спрайтов противников добавляется новый.
            enemies_sprites.add(Enemy(randint(20, 1000 - 20 - 128)))  # Появляется в случайном месте относительно
# .                                                                     горизонтали.
    for element in enemies_sprites:
        if pygame.sprite.spritecollideany(element, spaceships):
            run = False  # При столкновении игрока с противником, игра сразу завершается.
        for element_1 in lasers_sprites:  # Проверка каждого лазера и каждого корабля на столкновение друг с другом.
            if pygame.sprite.spritecollideany(element, lasers_sprites):
                enemies_sprites.remove(element)  # Если лазер столкнулся с противником, оба объекта удаляются из групп,
                lasers_sprites.remove(element_1)  # а счёт увеличивается на 1 очко.
                score += 1
        if pygame.sprite.spritecollideany(element, horizontal_border_up):
            enemies_sprites.remove(element)  # При столкновении противника с верхней границей отнимается жизнь.
            lifes -= 1  # Нужно для того, чтобы игрок не мог просто пропускать корабли мимо себя.

    for element in lasers_sprites:  # При столкновении лазера с границей лазер удаляется из группы спрайтов.
        if pygame.sprite.spritecollideany(element, horizontal_border_down):
            lasers_sprites.remove(element)

    keys = pygame.key.get_pressed()  # Управление кораблём.
    if keys[pygame.K_a]:
        if spaceship.rect.x > 20:  # Обозначил рамку, за которую не может вылетать игрок.
            spaceship.rect.x -= spaceship.player_speed
            spaceship.left = True
            spaceship.right = False  # right и left нужны были для смены картинок корабля, чтобы он наклонялся
    elif keys[pygame.K_d]:  # .        при движении.
        if spaceship.rect.x + WIDTH < size - 20:  # Обозначил рамку, за которую не может вылетать игрок.
            spaceship.rect.x += spaceship.player_speed
            spaceship.right = True
            spaceship.left = False
    else:
        spaceship.right = False
        spaceship.left = False

    if freeze:
        pause()  # Пытался реализовать паузу.

    if lifes == 0:
        run = False  # Если жизни заканчиваются, игра останавливается.

    draw()  # В конце цикла отрисовываются все объекты.

pygame.quit()
