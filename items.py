from threading import Timer

class Item:

    def __init__(self, key, name, description):
        self.key = key
        self.name = name
        self.description = description

    def use(self, player):
        pass

class SpecialItem(Item):
    
    def __init__(self, key, name, description):
        super().__init__(key, name, description)

    def use(self, player):
        pass

class Inventory:

    def __init__(self, owner):
        self.owner = owner
        self.items = []
        self.active = []

    def add(self, item: Item):
        self.items.append(item)
        if not isinstance(item, SpecialItem):
            self.active.append(item)

class InvincibilityPot(Item):
    
    def __init__(self):
        super().__init__("A0", "Invincibility Potion",
                         "Temporal immortality!")
        self.using = False

    def use(self, player):
        if self.using or player.invincible or player.drank: return
        self.using = True
        player.invincible = True
        player.drank = True
        t = Timer(5, self.cancel, [player])
        t.start()

    def cancel(self, player):
        player.invincible = False
        self.using = False

class LemonJuice(Item):
    
    def __init__(self):
        super().__init__("A1", "Lemon Juice", "Go faster!")
        self.using = False

    def use(self, player):
        if self.using or player.lemoned: return
        self.using = True
        player.lemoned = True
        player.speedmod = 2
        t = Timer(5, self.cancel, [player])
        t.start()

    def cancel(self, player):
        player.speedmod = 1
        self.using = False

class BowArrow(Item):
    
    def __init__(self):
        super().__init__("A2", "Bow and Arrow", "Bullseye!")
        self.using = False

    def use(self, player):
        if self.using: return
        self.using = True
        if player.heading() == 0.0:
            direction = "right"
        elif player.heading() == 90.0:
            direction = "up"
        elif player.heading() == 180.0:
            direction = "left"
        elif player.heading() == 270.0:
            direction = "down"
        player.shoot_arrow(direction)
        self.using = False
        # TODO: Fire arrow to enemy, make a new turtle?

class CannedJellyfish(Item):
    
    def __init__(self):
        super().__init__("A3", "Canned Jellyfish", "Tastes superb!")

    def use(self, player):
        if player.healed:
            return
        player.get_player().hp = 5
        player.healed = True

class Raft(SpecialItem):
    
    def __init__(self):
        super().__init__("FE", "Raft", "Traverse the waters!")

    def use(self, player):
        player.get_player().can_swim = True