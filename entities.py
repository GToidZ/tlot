import random
from turtle import Turtle
from items import Inventory, SpecialItem
from cartography import GameWorld, WaterRegion
import util

class Player:

    def __init__(self, name: str, world: GameWorld):
        self.name = name
        self.world = world
        self.score = 0
        self.tier = 0
        self.xp = 0
        self.hp = 5
        self.region = world.spawnpoint.copy()

        self.can_swim = False

        self.inventory = Inventory(self)

        self.x = 768 / 2
        self.y = 640 / 2

    def check_exp(self):
        required = [20, 30, 40]
        if self.tier >= 3:
            return
        if self.xp == required[self.tier]:
            self.tier += 1
            self.xp = 0

class PlayerController(Turtle):

    def __init__(self, root, player: Player, x, y):
        super().__init__("turtle", 0, True)
        self.turtlesize(1.5, 1.5)
        self.color(1, 1, 1)
        self.penup()
        self.speed(0)
        self.root = root
        self.player = player
        self.speedmod = 1
        self.attacking = False
        self.invincible = False
        self.healed = False
        self.__new_region = False

        self.goto(x, y)
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
                self.__new_region = True
            return
        self.goto(self.xcor(), self.ycor() + 32 * self.speedmod)
        if self.ycor() >= 640.0:
            self.goto(self.xcor(), self.ycor() - (self.ycor() - 640))
        self.update_coords()
        if self.__new_region:
            util.update_region(self.root, self.player, self.player.world)

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
                self.__new_region = True
            return
        self.goto(self.xcor(), self.ycor() - 32 * self.speedmod)
        if self.ycor() <= 0.0:
            self.goto(self.xcor(), 0.0)
        self.update_coords()
        if self.__new_region:
            util.update_region(self.root, self.player, self.player.world)

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
                self.__new_region = True
            return
        self.goto(self.xcor() - 32 * self.speedmod, self.ycor())
        if self.xcor() <= 0.0:
            self.goto(0.0, self.ycor())
        self.update_coords()
        if self.__new_region:
            util.update_region(self.root, self.player, self.player.world)

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
                self.__new_region = True
            return
        self.goto(self.xcor() + 32 * self.speedmod, self.ycor())
        if self.xcor() >= 768.0:
            self.goto(self.xcor() - (self.xcor() - 768), self.ycor())
        self.update_coords()
        if self.__new_region:
            util.update_region(self.root, self.player, self.player.world)

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

    def attack(self):
        if self.attacking:
            return
        self.attacking = True
        direction = self.heading()
        particle = Turtle("arrow", 0, False)
        particle.color("white")
        particle.speed(0)
        particle.penup()
        particle.setheading(direction - 90)
        if direction == 0.0:
            particle.goto(self.xcor() + 32, self.ycor() + 16)
            self.attack_particle(particle)
        if direction == 90.0:
            particle.goto(self.xcor() - 16, self.ycor() + 32)
            self.attack_particle(particle)
        if direction == 180.0:
            particle.goto(self.xcor() - 32, self.ycor() - 16)
            self.attack_particle(particle)
        if direction == 270.0:
            particle.goto(self.xcor() + 16, self.ycor() - 32)
            self.attack_particle(particle)
        self.damage(self.root)
        self.attacking = False

    def damage(self, root):
        direction = self.heading()
        if direction == 0.0:
            pos = [self.xcor() + 32, self.ycor()]
        if direction == 90.0:
            pos = [self.xcor(), self.ycor() + 32]
        if direction == 180.0:
            pos = [self.xcor() - 32, self.ycor()]
        if direction == 270.0:
            pos = [self.xcor(), self.ycor() - 32]
        if pos in root.entities.values():
            sel = [k for k, v in root.entities.items() if v == pos]
            for e in sel:
                if isinstance(e, Enemy):
                    dmg_out = self.player.tier + 1
                    e.hp -= dmg_out
                    if not e.dead:
                        e.check_dead(self.player)

    def attack_particle(self, particle):
        particle.speed(3)
        particle.pendown()
        particle.pensize(8)
        particle.fd(32)
        particle.clear()
        particle.penup()

    def check_dead(self):
        if self.player.hp <= 0:
            util.game_over(self.root, self.player, self.player.world)

    def update_coords(self):
        self.player.x = self.xcor()
        self.player.y = self.ycor()

    def set_coords(self, x, y):
        self.goto(x, y)
        self.update_coords()

    def get_player(self):
        return self.player

class Entity(Turtle):
    
    def __init__(self, x, y, shape="turtle", hp=0, has_brain=False):
        super().__init__(shape, 0, True)
        self.speed(0)
        self.penup()
        self.goto(x, y)
        self.x = x
        self.y = y
        self.hp = hp
        self.has_brain = has_brain

    def hit(self, target):
        pass

class ItemEntity(Entity):

    def __init__(self, x, y, item):
        super().__init__(x, y, "circle")
        colors = ["green", "blue", "yellow", "magenta"]
        self.color(random.choice(colors))
        self.collected = False
        self.item = item

    def hit(self, player):
        if self.collected:
            return
        player.get_player().inventory.add(self.item)
        if isinstance(self.item, SpecialItem):
            self.item.use(player)
        self.hideturtle()
        self.collected = True

class Enemy(Entity):
    
    def __init__(self, x, y, tier, root):
        super().__init__(x, y, "turtle", (tier+1)*2, True)
        self.color("red")
        self.turtlesize(1.5, 1.5)
        self.dead = False
        self.tier = tier
        self.behavior_seed = random.randint(10, 40)
        self.root = root

    def hit(self, player):
        if player.invincible or self.dead:
            return
        dmg_out = (self.tier - player.get_player().tier) + 1
        if dmg_out <= 0:
            dmg_out = 1
        player.get_player().hp -= dmg_out
        player.check_dead()
        player.invincible = True
        if self.heading() == 0.0:
            player.set_coords(player.xcor() + 64, player.ycor())
        if self.heading() == 90.0:
            player.set_coords(player.xcor(), player.ycor() + 64)
        if self.heading() == 180.0:
            player.set_coords(player.xcor() - 64, player.ycor())
        if self.heading() == 270.0:
            player.set_coords(player.xcor(), player.ycor() - 64)
        player.invincible = False

    def work(self):
        if self.root.elapsed % self.behavior_seed == 0:
            self.random_stroll()

    def random_stroll(self):
        i = random.randint(0, 1)
        if i == 0:
            if self.heading() == 0.0:
                if self.x + 32.0 > 768.0:
                    return
                self.x += 32.0
            if self.heading() == 90.0:
                if self.y + 32.0 > 640.0:
                    return
                self.y += 32.0
            if self.heading() == 180.0:
                if self.x - 32.0 < 0.0:
                    return
                self.x -= 32.0
            if self.heading() == 270.0:
                if self.y - 32.0 < 0.0:
                    return
                self.y -= 32.0
            self.forward(32)
        elif i == 1:
            j = random.randint(0, 2)
            if j == 0:
                self.left(90)
            if j == 1:
                self.right(90)
            if j == 2:
                self.left(180)

    def check_dead(self, player):
        if self.hp <= 0:
            self.dead = True
            self.hideturtle()
            player.score += (self.tier + 1) * 100
            if self.tier >= player.tier:
                player.xp += 1
            player.check_exp()