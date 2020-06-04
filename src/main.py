import pyglet

class Window(pyglet.window.Window):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.label.draw()

class Application:
    def __init__(self):
        self.window = Window()

    def run(self):
        pyglet.app.run()

def main():
    Application().run()

if __name__ == "__main__":
    main()