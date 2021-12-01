from turtle import Turtle

class Entity(Turtle):

    def __init__(self, has_collision=False, hitbox_size=8):
        self.has_collision = has_collision
        self.hitbox_size = hitbox_size

    def collide(self, touched):
        if not self.has_collision:
            return False
        else:
            self.on_collide(touched)

    def on_collide(self, target):
        pass

class LivingEntity(Entity):

    def __init__(self, max_health):
        super().__init__(True)
        self.max_health = max_health
        self.health = max_health

    def is_dead(self):
        return self.health <= 0

class Item:

    def __init__(self, key, name, description, sprite):
        self.key = key
        self.name = name
        self.description = description
        self._sprite = sprite

    def use(self):
        pass

class Inventory:

    def __init__(self, owner):
        self.owner = owner
        self.items = []
        self.equipped = {"q": None, "e": None}

    def add(self, item: Item):
        self.items.append(item)

    def equip(self, item: Item, slot):
        if not (slot == "q" or slot == "e"):
            raise ValueError("Slot must be either 'q' or 'e'.")
        self.equipped[slot] = item

    def takeoff(self, slot):
        if not (slot == "q" or slot == "e"):
            raise ValueError("Slot must be either 'q' or 'e'.")
        if not isinstance(self.equipped[slot], type(None)):
            self.equipped[slot] = None

    def remove(self, item: Item):
        if item in self.items:
            self.items.remove(item)
