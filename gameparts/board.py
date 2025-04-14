from .lib_graph import GameObject, Pic_seq, Sprite


class Board(GameObject):
    """Объект отрисовки и анимирования игрового поля"""

    def __init__(self, screen, sprite_size: int, width: int, height: int,
                 pic_name: str, sec_per_pic: float = 0.2):
        """Подгружает фоновые картинки и устанавливает скорость анимации
        и размеры игрового поля (в спрайтах)."""
        super().__init__(sprite_size, width, height)

        self.fon_pics = Pic_seq(pic_name, sec_per_pic, sprite_size)
        self.board = []

        # Заполнение игрового поля спрайтами
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Sprite(x * sprite_size, y * sprite_size,
                            sprite_size, screen))
            self.board.append(line)

    def draw(self):
        # Смена картинки для анимации
        self.fon_pics.next

        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x].draw(self.fon_pics())

    def __str__(self):
        return f"Board: {self.width=} {self.height}"


if __name__ == '__main__':
    import pygame

    clock = pygame.time.Clock()
    # Инициализировать библиотеку Pygame.
    pygame.init()
    # Создать окно размером 800x600 точек (или пикселей).
    screen = pygame.display.set_mode((810, 610))
    # Задать окну заголовок.
    pygame.display.set_caption('board.py')
    board = Board(screen, 20, 800 // 20, 600 // 20,
                  './pics/fon_01.png', 0.2)

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
        pygame.display.update()
        clock.tick(60)
    # Деинициализирует все модули pygame, которые были инициализированы ранее.
    pygame.quit()
