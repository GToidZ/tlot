import time

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
        print(self.items, self.active)

class InvisibilityPot(Item):
    
    def __init__(self):
        super().__init__("A0", "Invisibility Potion", "Turn invisible in just a sip.")

    def use(self, player):
        print(f"[{player.player.name}] used Invisibilty Potion")
        player.hideturtle()
        self.playeffect(player)

    def playeffect(self, player):
        target = time.time() + 10
        while time.time() < target:
            pass
        player.showturtle()