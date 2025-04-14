import pygame
from time import perf_counter

from gameparts import BoardIsFull
from gameparts import SnakeOutOfBorder
from gameparts import SnakeEatsItself

from gameparts import Board
from gameparts import Snake
from gameparts import Apple
# Размер квадратика игрового поля
SPRITE_SIZE = 50
SPRITES_WIDTH = 32
SPRITES_HIGHT = 20
# За сколько секунд происходит одно движение змеи
SECONDS_PER_MOVE = 0.2


class Game():
    """Класс, реализующий игру "Змейка"
    """
    def __init__(self, seconds_per_move,
                 sprite_size, sprite_width, sprite_hight):

        # Время одного движения змеи
        self.seconds_per_move = seconds_per_move
        # Размер ячейки поля
        self.sprite_size = sprite_size
        # Размер поля в ячейках в ширину
        self.sprite_width = sprite_width
        # Размер поля в ячейках в высоту
        self.sprite_hight = sprite_hight

        pygame.init()
        # Создать окно
        self.screen = pygame.display.set_mode(
            (sprite_width * sprite_size, sprite_hight * sprite_size))

        self.last_record = 0
        self.reset()

    def reset(self):
        """ Установка игры в начальное состояние"""
        self.board = Board(self.screen, self.sprite_size, self.sprite_width,
                           self.sprite_hight, './pics/fon_01.png', 0.2)
        self.snake = Snake(self.screen, self.sprite_size, self.sprite_width,
                           self.sprite_hight, self.sprite_width // 2,
                           self.sprite_hight // 2, direction='l')
        self.apple = Apple(self.screen, self.sprite_size,
                           self.sprite_width, self.sprite_hight)
        self.apple.set(1, 1)
        # Задать окну заголовок.
        pygame.display.set_caption('Snake')

    def cycle(self):
        """Основной цикл игры"""
        clock = pygame.time.Clock()
        old_time = perf_counter()

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
            self.board.draw()

            self.snake.set_buf_direction(cmd)

            new_time = perf_counter()
            dlt_time = new_time - old_time
            # Ограничиваем скорость движения змеи
            if dlt_time >= self.seconds_per_move:
                self.snake.set_from_buf_direction()

                if self.apple.is_apple_position(*self.snake.next_pos):
                    print('APPLE !!!!')
                    self.apple.remove()
                    self.snake.move('A')
                    self.apple.set_random(self.snake.snake_to_txt())

                    # Обновление рекорда
                    if len(self.snake.pos) > self.last_record:
                        self.last_record = len(self.snake.pos)

                    # Отображение статистики
                    pygame.display.set_caption('Last record: ' +
                                               str(self.last_record) +
                                               '    !!! SNAKE !!! ' +
                                               str(len(self.snake.pos)))
                    # print(self.apple)
                    # print(self.board)
                else:
                    self.snake.move()
                old_time = new_time

            self.snake.draw()
            self.apple.draw()
            pygame.display.update()

            # пытаемся отрисовывать 30 кадров в секунду
            clock.tick(30)

    def destructor(self):
        pygame.quit()


def main():
    game = Game(SECONDS_PER_MOVE, SPRITE_SIZE, SPRITES_WIDTH, SPRITES_HIGHT)

    play = True

    while play:
        play = False
        try:
            game.cycle()
        except BoardIsFull:
            game.reset()
            play = True
        except SnakeEatsItself:
            game.reset()
            play = True
        except SnakeOutOfBorder:
            game.reset()
            play = True

    game.destructor()


if __name__ == '__main__':
    main()
