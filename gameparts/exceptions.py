# Вот оно - новое исключение, унаследованное от базового класса Exception.
class BoardIsFull(Exception):
    def __init__(
        self,
        message='Некуда поставить яблоко. Вы победили!!!!'
    ):
        super().__init__(message)


class SnakeOutOfBorder(Exception):
    def __init__(
        self,
        message='Змея выползла за пределы доски. Вы проиграли!!!!'
    ):
        super().__init__(message)


class SnakeEatsItself(Exception):
    def __init__(
        self,
        message='Змея самоукусилась. Вы проиграли!!!!'
    ):
        super().__init__(message)
