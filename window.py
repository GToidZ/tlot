import turtle
import time
import entities
import cartography as car
import util

class Game:
    """ The root for the Turtle to run on.
    """
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
        
        self.elapsed = 0
        self.entities = {}
        
        self.save = ""

    def tick(self):
        # Updates the entire game
        self.update_screen()
        self._screen.logic()

    def update_screen(self):
        # Update frames in a rate of target FPS. (self.__fps)
        while time.time() < self._time + (1.0 / self.__fps):
            pass
        self.elapsed += 1
        turtle.update()
        self._time = time.time()

    def change_screen(self, screen):
        """ Clear the entire turtle program and renders a new screen.
        """
        if not isinstance(screen, GameScreen):
            raise TypeError(f"{screen} is not a GameScreen")
        self._screen = screen
        turtle.clearscreen()
        turtle.setworldcoordinates(0, 0, self.__width, self.__height)
        self.entities = {}
        screen.makescreen()
        turtle.listen()

    def refresh(self):
        """ Clear the entire turtle program and re-renders a screen.
        """
        turtle.clearscreen()
        turtle.setworldcoordinates(0, 0, self.__width, self.__height)
        self.entities = {}
        self._screen.makescreen()
        turtle.listen()

class GameScreen:
    """ A turtle Screen wrapper, with abstract render() and logic() method
    """
    keybinds = {}

    def __init__(self, root, bgcolor="black"):
        self.root = root
        self.bgcolor = bgcolor

    def makescreen(self):
        turtle.bgcolor(self.bgcolor)
        self.render()

    def render(self):
        """ Fires once the screen has been made.
        """
        pass

    def logic(self):
        """ Fires every game tick.
        """
        pass

    def register_keybind(self, key, event, description=""):
        """ Registers keybind to a function
        """
        self.keybinds[key] = description
        turtle.onkey(event, key)

class MenuScreen(GameScreen):
    """ Menu screen for the game.
    """
    def __init__(self, root):
        super().__init__(root)
        self.choice = 0
        self.turtles = []
        self.choices = {}

    def add_choice(self, x, y, label, fun):
        """ Add a choice to the main menu.
        Creates new turtle and registering it with a label.
        """
        choice_bullet = turtle.Turtle("circle", 0, False)
        choice_bullet.speed(0)
        choice_bullet.shapesize(1, 1)
        choice_bullet.penup()
        choice_bullet.color("white")
        choice_bullet.goto(x, y)
        choice_bullet.write(label, align="left", font=("Arial", 16, "normal"))
        choice_bullet.color("yellow")
        choice_bullet.goto(x - 32, y + 12)
        self.turtles.append(choice_bullet)
        self.choices[str(len(self.turtles) - 1)] = fun

    def update(self):
        for t in self.turtles:
            if self.turtles.index(t) == self.choice:
                t.showturtle()
            else:
                t.hideturtle()

    def moveup(self):
        """ Moves the bullet up.
        """
        if self.choice <= 0:
            self.update()
            return
        self.choice -= 1
        self.update()

    def movedown(self):
        """ Moves the bullet down.
        """
        if self.choice >= len(self.turtles) - 1:
            self.update()
            return
        self.choice += 1
        self.update()

    def select(self):
        """ Executes the selected choice.
        """
        self.choices[str(self.choice)]()

    def new_game(self):
        """ Fires new game event.
        """
        if not util.new_game(self.root):
            self.choice = 0
            self.turtles = []
            self.choices = {}
            self.root.refresh()

    def load_game(self):
        """ Fires load game event.
        """
        if not util.load_game(self.root):
            self.choice = 0
            self.turtles = []
            self.choices = {}
            self.root.refresh()

    def exit(self):
        """ Exits the program.
        """
        turtle.bye()

    def render(self):
        logo = turtle.Turtle(undobuffersize=0, visible=False)
        logo.speed(0)
        logo.color("white")
        logo.penup()
        logo.goto(384, 576)
        logo.write("The Legend of Tao", align="center", font=("Arial", 48, "normal"))
        self.add_choice(384 - 32, 192, "New Game", self.new_game)
        self.add_choice(384 - 32, 192 - 32, "Continue", self.load_game)
        self.add_choice(384 - 32, 192 - 64, "Exit", self.exit)
        self.register_keybind("Up", self.moveup)
        self.register_keybind("Down", self.movedown)
        self.register_keybind("space", self.select)
        self.register_keybind("Return", self.select)
        self.register_keybind("Escape", self.exit)
        self.update()

class PlayingScreen(GameScreen):
    """ A screen of the gameplay.
    """
    def __init__(self, root, player, world):
        super().__init__(root)
        self.player = player
        self.world = world
        
        self.curr_score = player.score
        self.curr_hp = player.hp
        self.curr_items = player.inventory.active

    def render(self):
        self.draw_background()
        self.create_player(self.root, self.player.x, self.player.y)
        self.ts, self.th, self.ti = self.draw_ui()

    def create_player(self, root, x, y):
        """ Creates a player at the x, y of screen and assign keybinds.
        """
        self.controller = entities.PlayerController(root, self.player, x, y)
        self.register_keybind("w", self.controller.move_up)
        self.register_keybind("a", self.controller.move_left)
        self.register_keybind("s", self.controller.move_down)
        self.register_keybind("d", self.controller.move_right)
        self.register_keybind("1", self.controller.use_item_one)
        self.register_keybind("2", self.controller.use_item_two)
        self.register_keybind("3", self.controller.use_item_three)
        self.register_keybind("4", self.controller.use_item_four)
        self.register_keybind("space", self.controller.attack)
        self.register_keybind("Escape", self.save)

    def draw_background(self):
        """ Draws game background with color according to Region types.
        """
        region = self.player.region
        map_pointer = self.world.get_region(region[0], region[1])
        color = "white"
        if isinstance(map_pointer, car.WaterRegion):
            color = "#64B0FE"
        elif isinstance(map_pointer, (car.SpawnRegion, car.GrasslandRegion)):
            color = "#89D900"
        elif isinstance(map_pointer, (car.PlateauRegion)):
            color = "#EB9F23"
        elif isinstance(map_pointer, (car.ForestRegion)):
            color = "#0D9400"
        elif isinstance(map_pointer, (car.MountainsRegion)):
            color = "#666666"
        elif isinstance(map_pointer, (car.JungleRegion)):
            color = "#004F08"
        elif isinstance(map_pointer, (car.SnowRegion)):
            color = "#48CEDF"
        elif isinstance(map_pointer, (car.DesertRegion)):
            color = "#E5E695"
        painter = turtle.Turtle("circle", 0, False)
        painter.speed(0)
        painter.color("black", color)
        painter.penup()
        painter.goto(-60, -60)
        painter.pendown()
        painter.begin_fill()
        for _ in range(2):
            painter.forward(828)
            painter.left(90)
            painter.forward(720)
            painter.left(90)
        painter.end_fill()

    def add_entity(self, entity):
        """ Register new entity to the screen for tracking.
        """
        self.root.entities[entity] = [entity.x, entity.y]

    def draw_ui(self):
        """ Draws UI components.
        """
        score = turtle.Turtle("circle", 0, False)
        hp = turtle.Turtle("circle", 0, False)
        items = turtle.Turtle("circle", 0, False)
        score.penup()
        hp.penup()
        items.penup()
        score.color("white")
        hp.color("white")
        items.color("white")
        score.speed(0)
        hp.speed(0)
        items.speed(0)
        score.goto(384, 700)
        score.write(str(self.curr_score), align="center", font=("Arial", 24, "normal"))
        hp.goto(192, 700)
        hp.write(f"HP: {self.curr_hp}", align="left", font=("Arial", 12, "normal"))
        items.goto(576, 700)
        items.write(self.construct_items_string(), align="right", font=("Arial", 12, "normal"))
        return score, hp, items
        
    def construct_items_string(self):
        res = ""
        for i in self.player.inventory.active:
            res += i.name[0].upper()
        if len(res) < 4:
            res += " "*(4 - len(res))
        if self.player.can_swim:
            res += "   R"
        else:
            res += "    "
        return res

    def update_ui(self, score, hp, items):
        """ Updates UI components every tick.
        """
        if self.curr_score != self.player.score:
            self.curr_score = self.player.score
            score.clear()
            score.write(str(self.curr_score), align="center", font=("Arial", 24, "normal"))
        if self.curr_hp != self.player.hp:
            self.curr_hp = self.player.hp
            if self.curr_hp <= 1:
                hp.color("red")
            else:
                hp.color("white")
            hp.clear()
            hp.write(f"HP: {self.curr_hp}", align="left", font=("Arial", 12, "normal"))
        if self.curr_items != self.player.inventory.items:
            self.curr_items = self.player.inventory.items
            items.clear()
            items.write(self.construct_items_string(), align="right", font=("Arial", 12, "normal"))            

    def save(self):
        """ Fires a save game event.
        """
        util.save_game(self.root, self.player, self.world)

    def logic(self):
        self.update_ui(self.ts, self.th, self.ti)
        if len(self.root.entities) != 0:
            for e in self.root.entities:
                self.root.entities[e] = [e.x, e.y]
                if e.has_brain:
                    e.work()
            pos = [self.player.x, self.player.y]
            if pos in self.root.entities.values():
                sel = [k for k, v in self.root.entities.items() if v == pos]
                for e in sel:
                    e.hit(self.controller)

class GameOverScreen(GameScreen):
    """ A screen displaying Game Over in red and final score.
    """
    def __init__(self, root, player):
        super().__init__(root)
        self.player = player

    def render(self):
        title = turtle.Turtle("circle", 0, False)
        title.speed(0)
        title.penup()
        title.goto(384, 384)
        title.color("red")
        title.write("Game Over", align="center",
                             font=("Arial", 48, "normal"))
        title.goto(384, 384 - 64)
        title.color("white")
        title.write(f"Final Score: {self.player.score}", align="center",
                             font=("Arial", 16, "normal"))
        title.goto(384, 384 - 64 - 32)
        title.color("white")
        title.write("Press ESC to exit", align="center",
                             font=("Arial", 16, "normal"))

        self.register_keybind("Escape", self.exit)
        
    def exit(self):
        turtle.bye()