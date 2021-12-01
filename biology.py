from core import LivingEntity, Inventory

class Player(LivingEntity):
    
    def __init__(self):
        self.__score = 0
        self.__coords = [0, 0]
        self.__inv = Inventory(self)
        self.x = 0
        self.y = 0
