from .lib_graph import GameObject, Pic_seq, Sprite
from copy import deepcopy
from .exceptions import SnakeEatsItself
# from .exceptions import SnakeOutOfBorder
# from icecream import ic
# ic.configureOutput(includeContext=True)


class Snake(GameObject):
    def __init__(self, screen, sprite_size, width, height,
                 x, y, direction='l'):
        super().__init__(sprite_size, width, height)
        self.board = []
        self.pos = [(x, y)]
        self.direction = direction
        self.buf_direction = direction

        # Подгрузка картинок элементов змеи
        # h_ - (head)
        # b_ - (body)
        # t_ - (tail)
        # угловые элементы: сначало направление от угла до головы,
        # потом направление до хвоста. Пример: up_right
        # В комментарии перед каждым ресурсом прописана буква, которой
        # представляется картинка в текстовом представлении игрового поля
        if 'Блок ресурсов':
            # 1
            self.h_left = Pic_seq('./pics/head_left_01.png', 0.1,
                                  sprite_size, sprite_size)
            # 2
            self.b_left = Pic_seq('./pics/body_hor_01.png', 0.1,
                                  sprite_size, sprite_size)
            # 3
            self.t_left = Pic_seq('./pics/tail_left_01.png', 0.1,
                                  sprite_size, sprite_size)
            # 4
            self.h_right = Pic_seq('./pics/head_right_01.png', 0.1,
                                   sprite_size, sprite_size)
            # 5
            self.b_right = Pic_seq('./pics/body_hor_01.png', 0.1,
                                   sprite_size, sprite_size)
            # 6
            self.t_right = Pic_seq('./pics/tail_right_01.png', 0.1,
                                   sprite_size, sprite_size)
            # q
            self.h_up = Pic_seq('./pics/head_up_01.png', 0.1,
                                sprite_size, sprite_size)
            # w
            self.b_up = Pic_seq('./pics/body_up_01.png', 0.1,
                                sprite_size, sprite_size)
            # e
            self.t_up = Pic_seq('./pics/tail_up_01.png', 0.1,
                                sprite_size, sprite_size)
            # r
            self.h_dn = Pic_seq('./pics/head_dn_01.png', 0.1,
                                sprite_size, sprite_size)
            # t
            self.b_dn = Pic_seq('./pics/body_dn_01.png', 0.1,
                                sprite_size, sprite_size)
            # y
            self.t_dn = Pic_seq('./pics/tail_dn_01.png', 0.1,
                                sprite_size, sprite_size)
            # 7
            self.up_left = Pic_seq('./pics/up_left_01.png', 0.1,
                                   sprite_size, sprite_size)
            # 8
            self.left_up = Pic_seq('./pics/left_up_01.png', 0.1,
                                   sprite_size, sprite_size)
            # u
            self.right_dn = Pic_seq('./pics/right_dn_01.png', 0.1,
                                    sprite_size, sprite_size)
            # i
            self.dn_left = Pic_seq('./pics/dn_left_01.png', 0.1,
                                   sprite_size, sprite_size)
            # o
            self.up_right = Pic_seq('./pics/up_right_01.png', 0.1,
                                    sprite_size, sprite_size)
            # p
            self.dn_right = Pic_seq('./pics/dn_right_01.png', 0.1,
                                    sprite_size, sprite_size)
            # h
            self.left_dn = Pic_seq('./pics/left_dn_01.png', 0.1,
                                   sprite_size, sprite_size)
            # j
            self.right_up = Pic_seq('./pics/right_up_01.png', 0.1,
                                    sprite_size, sprite_size)
        # Заполнение игрового поля спрайтами
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Sprite(x * sprite_size, y * sprite_size,
                            sprite_size, screen))
            self.board.append(line)
        # текстовый массив для предварительной прорисовки змеи
        self.blank_txt = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(' ')
            self.blank_txt.append(line)

    @property
    def next_pos(self):
        """Возвращает кортеж поля, куда собирается переползти
        змея"""
        dx, dy = 0, 0
        if self.direction == 'l':
            dx = -1
        elif self.direction == 'r':
            dx = 1
        elif self.direction == 'u':
            dy = -1
        elif self.direction == 'd':
            dy = 1
        return (self.pos[0][0]+dx, self.pos[0][1]+dy)

    def set_buf_direction(self, new_dir):
        """Получает и валидирует смену направления движения
        змеи в буффер"""
        if new_dir == '':
            return
        if new_dir not in 'udlr':
            return
        if new_dir == 'u' and self.direction == 'd':
            return
        if new_dir == 'd' and self.direction == 'u':
            return
        if new_dir == 'l' and self.direction == 'r':
            return
        if new_dir == 'r' and self.direction == 'l':
            return
        self.buf_direction = new_dir
        return

    def set_from_buf_direction(self):
        """ Буфферезируем новую комманду, пока не даем змее двигаться"""
        self.direction = self.buf_direction

    def set_direction(self, new_dir):
        """Получает и валидирует смену направления движения
        змеи."""
        if new_dir == '':
            return
        if new_dir not in 'udlr':
            return
        if new_dir == 'u' and self.direction == 'd':
            return
        if new_dir == 'd' and self.direction == 'u':
            return
        if new_dir == 'l' and self.direction == 'r':
            return
        if new_dir == 'r' and self.direction == 'l':
            return
        self.direction = new_dir
        return

    def move(self, target=None):
        """Движение змеи, если на ее пути яблоко, то
        увеличиваем ее размер"""
        x, y = self.next_pos

        # Вариант конца игры от удара о границы поля
        # if (x < 0) or (y < 0) or (x >= self.width) or (y >= self.height):
        #     raise SnakeOutOfBorder

        # Вариант цикличного движения
        if x < 0:
            x += self.width
        if y < 0:
            y += self.height

        x %= self.width
        y %= self.height

        if (x, y) in self.pos[:-1]:
            raise SnakeEatsItself

        self.pos.insert(0, (x, y))
        if target != 'A':
            self.pos.pop()
        # print(f'{self.pos=}')

    def _compare(self, base, target, target_type):
        """функция определения взаимного
        положения квадратов(Спрайтов) поля:
        выше, ниже, правее, левее.
        target type
        h ead
        t ail

        H и T предназначены для хвоста"""
        if target[1] < base[1]:
            rez = 'u'
        if target[1] > base[1]:
            rez = 'd'
        if target[0] > base[0]:
            rez = 'r'
        if target[0] < base[0]:
            rez = 'l'
        if target[0] == 0 and base[0] == self.width - 1:
            rez = 'r'

        if target[0] == self.width-1 and base[0] == 0:
            rez = 'l'

        if (target[1] == 0 and base[1] == self.height - 1) or\
           (target[1] == self.height - 1 and base[1] == 0):
            if target_type == 'H':
                rez = 'u'
            elif target_type == 'T':
                rez = 'd'
            elif target_type == 'h':
                rez = 'd'
            elif target_type == 't':
                rez = 'u'

        return rez

    def snake_to_txt(self):
        """Представляем змею в тексовом пространстве с
        кодировкой нужной картинки"""
        txt = deepcopy(self.blank_txt)
        # print(f"{self.direction=}")
        # отображение правильноповернутой головы
        if self.direction == 'l':
            h = '1'
        elif self.direction == 'r':
            h = '4'
        elif self.direction == 'u':
            h = 'q'
        elif self.direction == 'd':
            h = 'r'
        txt[self.pos[0][1]][self.pos[0][0]] = h

        # отображение тела
        if len(self.pos) > 2:
            for i in range(1, len(self.pos) - 1):
                head_tail = self._compare(self.pos[i], self.pos[i-1], 'h') +\
                    self._compare(self.pos[i], self.pos[i+1], 't')
                if head_tail == 'ur':
                    b = 'o'
                elif head_tail == 'rd':
                    b = 'u'
                elif head_tail == 'dl':
                    b = 'i'
                elif head_tail == 'lu':
                    b = '8'
                elif head_tail == 'dr':
                    b = 'p'
                elif head_tail == 'ld':
                    b = 'h'
                elif head_tail == 'ul':
                    b = '7'
                elif head_tail == 'ru':
                    b = 'j'
                elif head_tail == 'rl':
                    b = '5'

                elif head_tail == 'lr':
                    b = '2'
                elif head_tail == 'ud':
                    b = 'w'
                elif head_tail == 'du':
                    b = 't'

                elif head_tail == 'll':
                    b = '5'
                elif head_tail == 'rr':
                    b = '5'

                if self.direction == 'u':
                    if head_tail == 'dd':
                        b = 'w'
                    elif head_tail == 'uu':
                        b = 'w'

                txt[self.pos[i][1]][self.pos[i][0]] = b

        # отображение хвоста
        if len(self.pos) > 1:
            tail = self._compare(self.pos[-1], self.pos[-2], 'H')
            if tail == 'u':
                t = 'e'
            elif tail == 'd':
                t = 'y'
            elif tail == 'l':
                t = '3'
            elif tail == 'r':
                t = '6'

            # if self.pos[-1][1] == 0 and self.direction == 'u':
            #     t = 'e'
            # if self.pos[-1][1] == self.width and self.direction == 'd':
            #     t = 'y'

            txt[self.pos[-1][1]][self.pos[-1][0]] = t
        return txt

    def draw(self):
        txt = self.snake_to_txt()
        for y in range(self.height):
            for x in range(self.width):
                if txt[y][x] == ' ':
                    continue
                elif txt[y][x] == '1':
                    el = self.h_left()
                elif txt[y][x] == '2':
                    el = self.b_left()
                elif txt[y][x] == '3':
                    el = self.t_left()
                elif txt[y][x] == '4':
                    el = self.h_right()
                elif txt[y][x] == '5':
                    el = self.b_right()
                elif txt[y][x] == '6':
                    el = self.t_right()
                elif txt[y][x] == 'q':
                    el = self.h_up()
                elif txt[y][x] == 'w':
                    el = self.b_up()
                elif txt[y][x] == 'e':
                    el = self.t_up()
                elif txt[y][x] == 'r':
                    el = self.h_dn()
                elif txt[y][x] == 't':
                    el = self.b_dn()
                elif txt[y][x] == 'y':
                    el = self.t_dn()
                elif txt[y][x] == '7':
                    el = self.up_left()
                elif txt[y][x] == '8':
                    el = self.left_up()
                elif txt[y][x] == 'u':
                    el = self.right_dn()
                elif txt[y][x] == 'i':
                    el = self.dn_left()
                elif txt[y][x] == 'o':
                    el = self.up_right()
                elif txt[y][x] == 'p':
                    el = self.dn_right()
                elif txt[y][x] == 'h':
                    el = self.left_dn()
                elif txt[y][x] == 'j':
                    el = self.right_up()

                self.board[y][x].draw(el)

    def get_head_position(self):
        """ Возвращает позицию головы змейки."""
        return self.pos[0]


if __name__ == '__main__':
    import pygame
    from time import perf_counter
    from .board import Board
    # Размер квадратика игрового поля
    SPRITE_SIZE = 50
    # За сколько секунд происходит одно движение змеи
    SECONDS_PER_MOVE = 0.6
    # Размер квадратика игрового поля
    SPRITE_SIZE = 50

    clock = pygame.time.Clock()
    old_time = perf_counter()

    # Инициализировать библиотеку Pygame.
    pygame.init()
    # Создать окно размером 800x600 точек (или пикселей).
    screen = pygame.display.set_mode((810, 610))
    # Задать окну заголовок.
    pygame.display.set_caption('snake.py')
    board = Board(screen, SPRITE_SIZE, 800 // SPRITE_SIZE, 600 // SPRITE_SIZE,
                  './pics/fon_01.png', 0.2)

    snake = Snake(screen, SPRITE_SIZE, 800 // SPRITE_SIZE, 600 // SPRITE_SIZE,
                  5, 5, direction='l')
    #  В тестовых целях задал большую змею
    snake.pos = [(5, 5), (5, 4), (5, 3), (5, 2)]

    running = True
    cmd = ''
    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cmd = 'l'
                elif event.key == pygame.K_RIGHT:
                    cmd = 'r'
                elif event.key == pygame.K_UP:
                    cmd = 'u'
                elif event.key == pygame.K_DOWN:
                    cmd = 'd'
        board.draw()

        snake.set_buf_direction(cmd)

        new_time = perf_counter()
        dlt_time = new_time - old_time
        # Ограничиваем скорость движения змеи
        if dlt_time >= SECONDS_PER_MOVE:
            snake.set_from_buf_direction()
            snake.move()
            old_time = new_time

        snake.draw()
        pygame.display.update()

        # пытаемся отрисовывать 60 кадров в секунду
        clock.tick(30)
    # Деинициализирует все модули pygame, которые были инициализированы ранее.
    pygame.quit()
