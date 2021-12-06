from turtle import Turtle
from items import Item, Inventory
from cartography import GameWorld, WaterRegion

class Player:

    def __init__(self, name: str, world: GameWorld):
        self.name = name
        self.world = world
        self.score = 0
        self.tier = 0
        self.xp = 0
        self.requirements = [20, 30, 40]
        self.region = world.spawnpoint

        self.can_swim = False
        self.can_escape = False

        self.inventory = Inventory(self)
        
        self.x = 0
        self.y = 0


class PlayerController(Turtle):

    def __init__(self, player: Player):
        super().__init__("turtle", 0, True)
        self.turtlesize(1.5, 1.5)
        self.color(1, 1, 1)
        self.penup()
        self.speed(0)
        self.player = player
        self.speedmod = 1
        self.invincible = False

        self.update_coords()

    def current_region(self):
        print(self.player.world.get_region(self.player.region[0], self.player.region[1]))

    def move_up(self):
        self.setheading(90)
        if self.ycor() >= 640.0:
            region = self.player.region
            check = self.player.world.get_region(region[0] - 1, region[1])
            if check:
                if isinstance(check, WaterRegion) and \
                    not self.player.can_swim:
                    return
                region[0] += -1
                self.goto(self.xcor(), 0.0)
            return
        self.goto(self.xcor(), self.ycor() + 32 * self.speedmod)
        if self.ycor() >= 640.0:
            self.goto(self.xcor(), self.ycor() - (self.ycor() - 640))
        self.update_coords()

    def move_down(self):
        self.setheading(270)
        if self.ycor() <= 0.0:
            region = self.player.region
            check = self.player.world.get_region(region[0] + 1, region[1])
            if check:
                if isinstance(check, WaterRegion) and \
                    not self.player.can_swim:
                    return
                region[0] += 1
                self.goto(self.xcor(), 640.0)
            return
        self.goto(self.xcor(), self.ycor() - 32 * self.speedmod)
        if self.ycor() <= 0.0:
            self.goto(self.xcor(), 0.0)
        self.update_coords()

    def move_left(self):
        self.setheading(180)
        if self.xcor() <= 0.0:
            region = self.player.region
            check = self.player.world.get_region(region[0], region[1] - 1)
            if check:
                if isinstance(check, WaterRegion) and \
                    not self.player.can_swim:
                    return
                region[1] += -1
                self.goto(768.0, self.ycor())
            return
        self.goto(self.xcor() - 32 * self.speedmod, self.ycor())
        if self.xcor() <= 0.0:
            self.goto(0.0, self.ycor())
        self.update_coords()
        
    def move_right(self):
        self.setheading(0)
        if self.xcor() >= 768.0:
            region = self.player.region
            check = self.player.world.get_region(region[0], region[1] + 1)
            if check:
                if isinstance(check, WaterRegion) and \
                    not self.player.can_swim:
                    return
                region[1] += 1
                self.goto(0.0, self.ycor())
            return
        self.goto(self.xcor() + 32 * self.speedmod, self.ycor())
        if self.xcor() >= 768.0:
            self.goto(self.xcor() - (self.xcor() - 768), self.ycor())
        self.update_coords()
        
    def use_item_one(self):
        self.use_item("1")

    def use_item_two(self):
        self.use_item("2")

    def use_item_three(self):
        self.use_item("3")

    def use_item_four(self):
        self.use_item("4")

    def use_item(self, key):
        if isinstance(key, str):
            try:
                key = int(key)
            except:
                raise ValueError("Binding for items must be a number")
        if key <= len(self.player.inventory.active):
            self.player.inventory.active[key - 1].use(self)

    def update_coords(self):
        self.player.x = self.xcor()
        self.player.y = self.ycor()

    def set_coords(self, x, y):
        self.goto(x, y)
        self.update_coords()

    def get_player(self):
        return self.player

""" class Entity(Turtle):
    
    def __init__(self, ) """