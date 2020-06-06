"""Geometric shapes to draw.
"""

from typing import Tuple
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
    RECT_GL_COL = [128]*12
    RECT_GL_COL2 = [75]*12

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = self.as_vertices()
        cx, cy = self.center()
        self.label = pyglet.text.Label(
            '0', font_size=15, x=cx, y=cy, font_name='Impact',
            anchor_x='center', anchor_y='center', color=AlphaColors.WHITE)

    def as_vertices(self):
        return [
            self.x, self.y,
            self.x + self.w, self.y,
            self.x + self.w, self.y + self.h,
            self.x, self.y + self.h
        ]

    def center(self):
        return (2*self.x + self.w)//2, (2*self.y + self.h)//2

    def set_label(self, val):
        self.label.text = val
        self.label.color = AlphaColors.get_color_for_adj(val)

    def draw(self, render_text):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', self.v), ('c3B', Rectangle.RECT_GL_COL if render_text and self.label.text != '?' else Rectangle.RECT_GL_COL2))
        if render_text:
            self.label.draw()