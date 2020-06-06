"""The main file that contains the pyglet.
"""

import pyglet
from shapes import Rectangle, AlphaColors
from game import Minesweeper

class Application(pyglet.window.Window):
    RECT_LEN = 40
    BORDER = 1

    TOP_SIZE = 50
    TOP_FONT_SIZE = 15
    TOP_H_OFFSET = 8
    TOP_V_OFFSET = -25

    WIDTH = Minesweeper.COL_SIZE * RECT_LEN
    HEIGHT = Minesweeper.ROW_SIZE * RECT_LEN + TOP_SIZE

    def __init__(self, *args, **kargs):
        """Create an application instance.
        """
        super().__init__(Application.WIDTH, Application.HEIGHT, *args, **kargs)
        self.game = None
        self.rects = [
            [
                Rectangle(
                    Application.BORDER + Application.RECT_LEN * r,
                    Application.BORDER + Application.RECT_LEN * c,
                    Application.RECT_LEN - 2 * Application.BORDER,
                    Application.RECT_LEN - 2 * Application.BORDER
                ) for c in range(Minesweeper.COL_SIZE)
            ] for r in range(Minesweeper.ROW_SIZE)
        ]
        self.label = pyglet.text.Label(
            "X", font_size=Application.TOP_FONT_SIZE,
            x=Application.WIDTH//2 + Application.TOP_H_OFFSET,
            y=Application.HEIGHT + Application.TOP_V_OFFSET,
            font_name='Impact', anchor_x='center',
            anchor_y='center', color = AlphaColors.RED
        )

    def center_window(self) -> None:
        """Place this window centrally on the display.
        """
        screen = pyglet.canvas.Display().get_default_screen()
        c_x = screen.width // 2 - self.width // 2
        c_y = screen.height // 2 - self.height // 2
        self.set_location(c_x, c_y)

    def on_draw(self) -> None:
        """Redraw everything.
        """
        self.clear()

        if self.game is None:
            for rows in self.rects:
                for r in rows:
                    r.draw(False)
        else:
            for r, row in enumerate(self.rects):
                for c, rect in enumerate(row):
                    if self.game.mat[r][c].is_visible():
                        adj = self.game.mat[r][c].adjacent_bombs()
                        rect.set_label('X' if adj == -1 else str(adj))
                        rect.draw(True)
                    elif self.game.mat[r][c].is_marked():
                        rect.set_label('?')
                        rect.draw(True)
                    else:
                        rect.draw(False)

            self.label.text = str(self.game.bombs_rem)
            self.label.draw()

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        """Event handler for mouse clicks.

        Args:
            x (int): X coordinate of mouse click.
            y (int): Y coordinate of mouse click
            button (int): What mouse button was pressed.
            _ (int): Modifiers. Unused.
        """
        _x, _y = x//Application.RECT_LEN, y//Application.RECT_LEN
        if _x < Minesweeper.ROW_SIZE and _y < Minesweeper.COL_SIZE:
            if self.game is None:
                self.game = Minesweeper(_x, _y)
            elif not self.game.is_over():
                if button == pyglet.window.mouse.LEFT:
                    self.game.left_click(_x, _y)
                elif button == pyglet.window.mouse.RIGHT:
                    self.game.right_click(_x, _y)
        else:
            self.game = None

def main() -> None:
    """Starting point.
    """
    app = Application("Minesweeper", resizable=False)
    app.center_window()
    pyglet.app.run()

if __name__ == "__main__":
    main()
