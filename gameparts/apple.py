from .lib_graph import GameObject, Pic_seq, Sprite
from random import choice
from .exceptions import BoardIsFull


class Apple(GameObject):
    """Объект Apple умеет ставится на игровой доске мимо змеи,
    сам себя анимирует"""

    def __init__(self, screen, sprite_size, width, height):
        super().__init__(sprite_size, width, height)
        self.apple_pic = Pic_seq('./pics/apple_01.png', 0.1,
                                 sprite_size, sprite_size)
        self.spritesize = sprite_size
        self.sprite = Sprite(10, 10, sprite_size, screen)
        # Установленно ли яблочко
        self.is_apple = False
        self.apple_x = 0
        self.apple_y = 0

    def draw(self):
        """Отрисовка, если существует, яблока в нужном позиции
        (с анимацией)."""
        if self.is_apple:
            self.apple_pic.next
            self.sprite.x = self.apple_x * self.spritesize
            self.sprite.y = self.apple_y * self.spritesize
            self.sprite.draw(self.apple_pic())

    @property
    def position(self):
        """Возвращает координаты яблока."""
        if self.is_apple:
            return (self.apple_x, self.apple_y)
        return None

    def is_apple_position(self, x, y):
        """Проверяет: существует ли по этим координатам яблоко."""
        if not self.is_apple:
            return False

        # Вариант цикличного движения
        if x < 0:
            x += self.width
        if y < 0:
            y += self.height

        x %= self.width
        y %= self.height

        if (x, y) == (self.apple_x, self.apple_y):
            return True
        return False

    def remove(self):
        """Удаляем яблоко"""
        self.is_apple = False

    def set(self, x, y):
        """Ручная установка яблока"""
        self.is_apple = True
        self.apple_x = x
        self.apple_y = y

    def text_to_list(self, text):
        """Формируем список кортежей координат ячеек, где
        не находится змея"""
        rez = []
        for y, line in enumerate(text):
            for x, el in enumerate(line):
                if el == ' ':
                    rez.append((x, y))
        return rez

    def set_random(self, text_snake):
        """Постановка яблока в случайной позиции доски,
        если нет свободного места(вся доска занята змеей), то
        вызывает исключение BoardIsFull"""
        rez = self.text_to_list(text_snake)
        if len(rez) == 0:
            raise BoardIsFull
        self.apple_x, self.apple_y = choice(rez)
        self.is_apple = True

    def __str__(self):
        return f"Apple: {self.is_apple=} {self.apple_x=} {self.apple_y=}"


if __name__ == '__main__':
    import pygame
    from .board import Board
    from time import perf_counter
    from .snake import Snake
    # Размер квадратика игрового поля
    SPRITE_SIZE = 50
    # За сколько секунд происходит одно движение змеи
    SECONDS_PER_MOVE = 0.6

    clock = pygame.time.Clock()
    old_time = perf_counter()

    # Инициализировать библиотеку Pygame.
    pygame.init()
    # Создать окно размером 800x600 точек (или пикселей).
    screen = pygame.display.set_mode((810, 610))
    # Задать окну заголовок.
    pygame.display.set_caption('apple.py')
    board = Board(screen, SPRITE_SIZE, 800 // SPRITE_SIZE, 600 // SPRITE_SIZE,
                  './pics/fon_01.png', 0.2)
    # snake = Snake(screen, SPRITE_SIZE, 800 // 20, 600 // 20,
    #               800 // 40, 600 // 40, direction='l')
    snake = Snake(screen, SPRITE_SIZE, 800 // SPRITE_SIZE, 600 // SPRITE_SIZE,
                  5, 5, direction='l')
    #  В тестовых целях задал большую змею
    snake.pos = [(5, 5), (5, 4), (5, 3), (5, 2)]
    apple = Apple(screen, SPRITE_SIZE, 800 // SPRITE_SIZE, 600 // SPRITE_SIZE)
    apple.set(2, 2)
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

            if apple.is_apple_position(*snake.next_pos):
                print('APPLE !!!!')
                apple.remove()
                snake.move('A')
                apple.set_random(snake.snake_to_txt())
                pygame.display.set_caption('apple.py ' + str(len(snake.pos)))
                print(apple)
                print(board)
            else:
                snake.move()
            old_time = new_time

        snake.draw()
        apple.draw()
        pygame.display.update()

        # пытаемся отрисовывать 60 кадров в секунду
        clock.tick(30)
    # Деинициализирует все модули pygame, которые были инициализированы ранее.
    pygame.quit()
