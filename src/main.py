import pyglet, sys
from random import uniform

class Colors:
    GRAY = (0,)*4
    COLOR_MAP = [
        GRAY, # -1
        GRAY, # 0 
        GRAY, # 1 
        GRAY, # 2 
        GRAY, # 3 
        GRAY, # 4 
        GRAY, # 5 
        GRAY, # 6 
        GRAY, # 7
        GRAY  # 8
    ]

    @staticmethod
    def get_color_for_adj(n):
        return Colors.COLOR_MAP[n+1]

        



class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = self.as_vertices()
        self.cx, self.cy = self.center() 

    def as_vertices(self):
        return [
            self.x, self.y,
            self.x + self.w, self.y,
            self.x + self.w, self.y + self.h,
            self.x, self.y + self.h
        ]

    def center(self):
        return (2*self.x + self.w)//2, (2*self.y + self.h)//2


class Application(pyglet.window.Window):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.rects = [] 
        self.labels = []
        self.label = pyglet.text.Label(
            "32", font_size=15, 
            x=320+8, y=640+8+35, font_name='Impact', anchor_x='center', anchor_y='center', color = (255,0,0,255))
        for x in range(16):
            for y in range(16):
                self.rects.append(Rectangle(x*40+x,y*40+y,40,40))
                cx,cy = self.rects[-1].center()
                self.labels.append(pyglet.text.Label(str(int(uniform(0,6))), font_size=15, x=cx, y=cy, font_name='Impact', bold = False, anchor_x='center', anchor_y='center', color = (255,0,0,255)))

    def on_draw(self):
        self.clear()
        
        for l, r in zip(self.labels, self.rects):
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', r.as_vertices()))
            l.draw()

        self.label.draw()

def main():
    screen = pyglet.canvas.Display().get_default_screen()
    app = Application(640+16,640+16+50,"Minesweeper",resizable=False)
    app.set_location(screen.width // 2 - app.width // 2, screen.height // 2 - app.height // 2)
    pyglet.app.run()

if __name__ == "__main__":
    main()


# 16 x 30, 99 sprengjur...