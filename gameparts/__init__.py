# gameparts/__init__.py.

# Точка в записи означает текущий каталог.
from .exceptions import BoardIsFull
from .exceptions import SnakeOutOfBorder
from .exceptions import SnakeEatsItself

from .apple import Apple
from .snake import Snake
from .board import Board
