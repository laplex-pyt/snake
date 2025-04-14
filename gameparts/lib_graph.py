import pygame
from time import perf_counter


class Pic_seq:
    """ Класс, загружающий набор картинок для возможности выдачи их
    с заданной частотой для анимирования"""
    def __init__(self, fname: str,
                 sec_per_pic=0.2, dim_x: int = 100, dim_y: int = 100):
        """Загрузка и масштабирование набора картинок
        - fname - имя первой картинки [name_01.png]
        - sec_per_pic минимальная задержка при смене картинки
        - dim_x, dim_y - желаемые размеры картинок
        - максимально загружается сет из 20 картинок
        """
        self.sec_per_pic = sec_per_pic
        # хранилище картинок анимации
        self.buf = []
        self.pointer = 0
        self.incrementator = 1
        self.now = perf_counter()
        try:
            for i in range(1, 21):
                fname = fname[:-6] + str(i).zfill(2) + fname[-4:]
                print(fname)
                image = pygame.image.load(fname).convert_alpha()
                new_image = pygame.transform.scale(image, (dim_x, dim_y))
                self.buf.append(new_image)
        except FileNotFoundError:
            print(f'загружено {i-1} картинок последовательности {fname[:-6]} ')

    @property
    def next(self):
        """смещает указатель на следующую картинку,
        вызывать можно как угодно часто, но смена картинки
        происходит не чаще, чем задано в параметре sec_per_pic"""
        new_time = perf_counter()
        dlt = new_time - self.now
        if dlt > self.sec_per_pic:
            if self.pointer == 0:
                self.incrementator = 1
            if self.pointer >= len(self.buf)-1:
                self.incrementator = -1

            self.pointer += self.incrementator
            self.now = new_time

    @property
    def pict(self):
        """Возвращает текущую картинку"""
        return self.buf[self.pointer]

    def __call__(self):
        """Возвращает текущую картинку"""
        return self.buf[self.pointer]


class Sprite:
    """Спрайт, квадратный участок экрана, на который можно выводить
    картинку"""
    def __init__(self, x: int, y: int, sprite_size: int, screen):
        """Сохраняются координаты прямоугольной области окна
        с координатами верхнего правого угла и размером sprite_size."""
        self.x = x
        self.y = y

        self.sprite_size = sprite_size
        self.screen = screen

    def draw(self, object=None):
        """Отрисовка в заданном спрайте картинки."""
        if object:
            self.screen.blit(object, (self.x, self.y))

    def is_click_in(self, x, y):
        """Проверка принадлежности данных координат окна данному
        спрайту. Полезно для определения нажатия мыши на спрайт"""
        if (self.x <= x <= self.x + self.sprite_size) and\
           (self.y <= y <= self.y + self.sprite_size):
            return True
        return False


class GameObject:
    """Базовый класс игровых объектов
    умеет отрисовывать себя"""
    def __init__(self, sprite_size: int, width: int, height: int,):
        """Сохраняет размер клетки игрового поля (Спрайта)."""
        self.spritesize = sprite_size
        self.width = width
        self.height = height

    def draw(self):
        """Метод отрисовки себя на экране"""
        ...
