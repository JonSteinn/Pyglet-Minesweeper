import pyglet
from shapes import Rectangle
from game import Minesweeper

class Application(pyglet.window.Window):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.game = None
        self.rects = [[Rectangle(1+40*r, 1+40*c, 38, 38) for c in range(16)] for r in range(16)]
        self.label = pyglet.text.Label(
            "32", font_size=15,
            x=320+8, y=640+8+25, font_name='Impact', anchor_x='center', anchor_y='center', color = (255,0,0,255))

    def on_draw(self):
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

    def on_mouse_press(self, x, y, button, modifiers):
        c = y//40
        r = x//40
        if r < 16 and c < 16:
            if self.game is None:
                self.game = Minesweeper(r,c)
            elif not self.game.is_over():
                if button == pyglet.window.mouse.LEFT:
                    self.game.left_click(r,c)
                elif button == pyglet.window.mouse.RIGHT:
                    self.game.right_click(r,c)
        else:
            self.game = None

def main():
    screen = pyglet.canvas.Display().get_default_screen()
    app = Application(640,640+50,"Minesweeper",resizable=False)
    app.set_location(screen.width // 2 - app.width // 2, screen.height // 2 - app.height // 2)
    pyglet.app.run()

if __name__ == "__main__":
    main()