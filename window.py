import turtle
import time

class Game:
    
    objects = []
    
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
        screen.makescreen()


class GameScreen:
    
    def __init__(self, bgcolor="black"):
        self.bgcolor = bgcolor

    def makescreen(self):
        turtle.bgcolor(self.bgcolor)
        self.render()

    def render(self):
        pass


""" class TestScreen(GameScreen):
    
    def __init__(self):
        super().__init__()

    def render(self):
        renderer = turtle.Turtle()
        renderer.color("white")

class TestScreen2(GameScreen):
    
    def __init__(self):
        super().__init__()
    
    def render(self):
        renderer_b = turtle.Turtle()
        renderer_b.color("red")
        renderer_b.fd(100) """
