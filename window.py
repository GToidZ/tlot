import turtle
import time
import entities

class Game:
    
    def __init__(self, view_width=768, view_height=768,
                 fps=60.0, title="The Legend of Tao"):
        self.__width = view_width
        self.__height = view_height
        self.__fps = fps

        turtle.setup(self.__width,
                     self.__height)
        turtle.title(title)
        turtle.tracer(0)
        turtle.ht()
        turtle.penup()
        turtle.setundobuffer(0)

        self._time = time.time()
        self._screen = None

    def tick(self):
        # Updates the entire game
        self.update_screen()

    def update_screen(self):
        # Update frames in a rate of target FPS. (self.__fps)
        while time.time() < self._time + (1.0 / self.__fps):
            pass
        turtle.update()
        self._time = time.time()

    def change_screen(self, screen):
        if not isinstance(screen, GameScreen):
            raise TypeError(f"{screen} is not a GameScreen")
        self._screen = screen
        turtle.clearscreen()
        turtle.setworldcoordinates(0, 0, self.__width, self.__height)
        screen.makescreen()
        turtle.listen()

class GameScreen:
    
    keybinds = {}

    def __init__(self, bgcolor="black"):
        self.bgcolor = bgcolor

    def makescreen(self):
        turtle.bgcolor(self.bgcolor)
        self.render()

    def render(self):
        pass

    def register_keybind(self, key, event, description=""):
        self.keybinds[key] = description
        turtle.onkey(event, key)

class PlayingScreen(GameScreen):
    
    def __init__(self, player):
        super().__init__()
        self.player = player

    def render(self):
        self.controller = entities.PlayerController(self.player)
        self.register_keybind("w", self.controller.move_up)
        self.register_keybind("a", self.controller.move_left)
        self.register_keybind("s", self.controller.move_down)
        self.register_keybind("d", self.controller.move_right)
        self.register_keybind("1", self.controller.use_item_one)
