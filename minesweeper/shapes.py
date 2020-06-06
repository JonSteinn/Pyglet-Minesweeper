"""Geometric shapes to draw.
"""

from typing import Tuple, List
import pyglet


class AlphaColors:
    """A static collection of color constants
    """

    GREEN = (0, 255, 0, 255)
    RED = (255, 0, 0, 255)
    BLUE = (0, 0, 255, 255)
    GRAY = (128, 128, 128, 255)
    YELLOW = (255, 255, 0, 255)
    PINK = (255, 0, 255, 255)
    BLACK = (0, 0, 0, 255)
    ORANGE = (255, 128, 0, 255)
    PURPLE = (102, 0, 102, 255)
    TEAL = (0, 128, 128, 255)
    WHITE = (255, 255, 255, 255)
    CYAN = (0, 255, 255, 255)
    OLIVE = (128, 128, 0, 255)
    BROWN = (139, 69, 19, 255)

    COLOR_MAP = {
        'X': RED,
        '0': WHITE,
        '1': GREEN,
        '2': YELLOW,
        '3': PINK,
        '4': BLUE,
        '5': BLACK,
        '6': PURPLE,
        '7': CYAN,
        '8': OLIVE,
        '?': RED
    }

    @staticmethod
    def get_color_for_adj(token: str) -> Tuple[int, int, int, int]:
        """Fetch the color chosen for a specific token.

        Args:
            token (str): The token to match with a color.

        Returns:
            Tuple[int, int, int, int]: rgba color value.
        """
        return AlphaColors.COLOR_MAP[token]


class Rectangle:
    """A rectangle drawing, possibl containing a centered label.
    """

    RECT_GL_COL = [128]*12
    RECT_GL_COL2 = [75]*12
    BOMB_TOKEN = '?'
    FONT_SIZE = 15

    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        """Create an instance of a drawable rectangle.

        Args:
            x (int): x coordinate of the lower left corner.
            y (int): y coordinate of the lower lef corner.
            w (int): width of the rectangle.
            h (int): height of the rectangle.
        """
        self.vertices: List[int] = Rectangle.as_vertices(x, y, w, h)
        c_x, c_y = Rectangle.center(x, y, w, h)
        self.label: pyglet.text.Label = pyglet.text.Label(
            '0', font_size=Rectangle.FONT_SIZE, x=c_x, y=c_y, font_name='Impact',
            anchor_x='center', anchor_y='center', color=AlphaColors.WHITE)

    @staticmethod
    def as_vertices(x: int, y: int, w: int, h: int) -> List[int]:
        """Create list of corner vertices of rectangle.

        Args:
            x (int): x coordinate of the lower left corner.
            y (int): y coordinate of the lower lef corner.
            w (int): width of the rectangle.
            h (int): height of the rectangle.

        Returns:
            List[int]: The list of vertices in gl quad format.
        """
        return [
            x, y,
            x + w, y,
            x + w, y + h,
            x, y + h
        ]

    @staticmethod
    def center(x: int, y: int, w: int, h: int) -> Tuple[int, int]:
        """Find the center of the rectangle.

        Args:
            x (int): x coordinate of the lower left corner.
            y (int): y coordinate of the lower lef corner.
            w (int): width of the rectangle.
            h (int): height of the rectangle.

        Returns:
            Tuple[int, int]: The center point of the rectangle.
        """
        return (2*x + w)//2, (2*y + h)//2

    def set_label(self, token: str) -> None:
        """Set the label of a square.

        Args:
            token (str): The label token for a square.
        """
        self.label.text = token
        self.label.color = AlphaColors.get_color_for_adj(token)

    def draw(self, render_text: bool) -> None:
        """Draw the rectangle. Rectangles with a visible token
        get a different base color.

        Args:
            render_text (bool): Should the label be drawn?
        """
        if render_text and self.label.text != Rectangle.BOMB_TOKEN:
            color = Rectangle.RECT_GL_COL
        else:
            color = Rectangle.RECT_GL_COL2
        pyglet.graphics.draw(
            4, pyglet.gl.GL_QUADS, ('v2f', self.vertices), ('c3B', color))
        if render_text:
            self.label.draw()
