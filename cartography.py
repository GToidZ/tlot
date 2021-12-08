from random import Random, choice
from time import time_ns
import items

class GameWorld:
    """ World class for sandboxing and simulating a game world.
    The world generation is based on Cellular Automata.
    """
    def __init__(self, seed=""):
        self.seed = seed
        self.__size = 24
        self.__prng = Random(self.seed)
        self.__islandmap = self.gen_geography()
        self.spawnpoint = self.select_spawnpoint()
        self.__tiermap = self.scale_tiers()
        self.__biomemap = self.populate_biomes()
        self.itemmap = self.place_items()

    @property
    def seed(self):
        return self.__seed
    @seed.setter
    def seed(self, seed):
        if not isinstance(seed, (str, int)):
            seed = self.gen_seed()
        if len(seed) < 6:
            seed = self.gen_seed()
        self.__seed = seed

    def get_prng(self):
        return self.__prng

    def gen_seed(self):
        """ Generates a 20-character length seed string.
        """
        fun = ["angel", "basalisk", "chimera", "cockatrice", "cyclops", "devil", \
            "goblin", "ogre", "pegasus", "phoenix", "unicorn"]
        return (choice(fun) + str(time_ns()))[:20]

    def gen_geography(self):
        """ Generates a new world map using Cellular Automata.
        """
        worldmap = CellAutoIsland(self.__size, self.__size, self.__prng)
        return worldmap.map

    def select_spawnpoint(self):
        """ Chooses a suitable spawnpoint.
        """
        while True:
            x = self.__prng.randint(6,self.__size - 6)
            y = self.__prng.randint(6,self.__size - 6)
            if not self.__islandmap[x][y]:
                return [x, y]

    def scale_tiers(self):
        """ Assigns each region of the world map with respective tiers.
        """
        center = self.spawnpoint
        tiermap = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        for x in range(self.__size):
            for y in range(self.__size):
                if abs(x - center[0]) > 12 \
                    or abs(y - center[1]) > 12:
                    tiermap[x][y] = 3
                elif abs(x - center[0]) > 8 \
                    or abs(y - center[1]) > 8:
                    tiermap[x][y] = 2
                elif abs(x - center[0]) > 4 \
                    or abs(y - center[1]) > 4:
                    tiermap[x][y] = 1
        return tiermap

    def get_tiermap(self):
        return self.__tiermap

    def populate_biomes(self):
        """ Assigns each region of the world map with respective biomes.
        """
        biomemap = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        for x in range(self.__size):
            for y in range(self.__size):
                if [x, y] == self.spawnpoint:
                    biomemap[x][y] = SpawnRegion()
                else:
                    if self.__islandmap[x][y]:
                        biomemap[x][y] = WaterRegion((self.__tiermap[x][y]))
                    else:
                        if self.__tiermap[x][y] == 0:
                            biomemap[x][y] = GrasslandRegion()
                        elif self.__tiermap[x][y] == 1:
                            if x < self.__size / 2:
                                biomemap[x][y] = PlateauRegion()
                            else:
                                biomemap[x][y] = ForestRegion()
                        elif self.__tiermap[x][y] == 2:
                            if x < self.__size / 2:
                                biomemap[x][y] = MountainsRegion()
                            else:
                                biomemap[x][y] = JungleRegion()
                        elif self.__tiermap[x][y] == 3:
                            if x < self.__size / 2:
                                biomemap[x][y] = SnowRegion()
                            else:
                                biomemap[x][y] = DesertRegion()
        return biomemap

    def place_items(self):
        """ Randomly places all items into the world map.
        """
        self.itemmap = {}
        all_items = [items.InvincibilityPot(),
                     items.LemonJuice(),
                     items.BowArrow(),
                     items.CannedJellyfish()]
        raft = items.Raft()
        while True:
            x = self.__prng.randint(6, self.__size - 6)
            y = self.__prng.randint(6, self.__size - 6)
            if not self.__islandmap[x][y] and self.__tiermap[x][y] == 0 \
                and [x, y] != self.spawnpoint:
                self.itemmap[raft] = self.spawnpoint
                break
        while len(all_items) > 0:
            item = all_items.pop(0)
            while True:
                x = self.__prng.randint(3, self.__size - 3)
                y = self.__prng.randint(3, self.__size - 3)
                if [x, y] not in self.itemmap.values():
                    self.itemmap[item] = [x, y]
                    break
        return self.itemmap

    def get_region(self, x, y):
        if any([x > len(self.__biomemap) - 1, x < 0,
                y > len(self.__biomemap[0]) - 1, y < 0]):
            return None
        return self.__biomemap[x][y]

    def ascii_map(self):
        """ Prints world map into the console for debugging purposes.
        """
        for x in range(self.__size):
            for y in range(self.__size):
                if [x, y] == self.spawnpoint:
                    print("X", end="")
                else:
                    if not self.__islandmap[x][y]:
                        print("#", end="")
                    else:
                        print(".", end="")
            print()
        for x in range(self.__size):
            for y in range(self.__size):
                if [x, y] == self.spawnpoint:
                    print("X", end="")
                else:
                    print(self.__tiermap[x][y], end="")
            print()
        for x in range(self.__size):
            for y in range(self.__size):
                if not self.__biomemap[x][y]:
                    print(" ", end="")
                else:
                    if isinstance(self.__biomemap[x][y], SpawnRegion):
                        print("*", end="")
                    if isinstance(self.__biomemap[x][y], WaterRegion):
                        print("~", end="")
                    if isinstance(self.__biomemap[x][y], GrasslandRegion):
                        print("G", end="")
                    if isinstance(self.__biomemap[x][y], PlateauRegion):
                        print("P", end="")
                    if isinstance(self.__biomemap[x][y], ForestRegion):
                        print("F", end="")
                    if isinstance(self.__biomemap[x][y], MountainsRegion):
                        print("M", end="")
                    if isinstance(self.__biomemap[x][y], JungleRegion):
                        print("J", end="")
                    if isinstance(self.__biomemap[x][y], SnowRegion):
                        print("S", end="")
                    if isinstance(self.__biomemap[x][y], DesertRegion):
                        print("D", end="")
            print()

class CellAutoIsland:
    """ An implementation of Cellular Automata to generate
    0s and 1s as a square grid. This algorithm can be finer down
    until we get an archipelago-like world.
    """
    def __init__(self, width, height, prng=Random()):
        self._width = width
        self._height = height
        self.__prng = prng
        self.map = self.make_map(self.__prng.randint(3,5))

    def make_grid(self):
        return [[0 for _ in range(self._width)] for _ in range(self._height)]

    def make_chunks(self, dest):
        chance = 0.4
        for x in range(self._width):
            for y in range(self._height):
                if self.__prng.random() < chance:
                    dest[x][y] = 1
        return dest

    def count_alive_neighbours(self, dest, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                nbx = x + i
                nby = y + j
                if i == 0 and j == 0:
                    pass
                elif nbx < 0 or nby < 0 or nbx >= len(dest) or nby >= len(dest[0]):
                    count += 1
                elif dest[nbx][nby]:
                    count += 1
        return count

    def simulate(self, orig, death, birth):
        dest = self.make_grid()
        for x in range(len(orig)):
            for y in range(len(orig[0])):
                nbs = self.count_alive_neighbours(orig, x, y)
                if orig[x][y]:
                    if nbs < death:
                        dest[x][y] = 0
                    else:
                        dest[x][y] = 1
                else:
                    if nbs > birth:
                        dest[x][y] = 1
                    else:
                        dest[x][y] = 0
        return dest

    def make_map(self, steps):
        result = self.make_grid()
        result = self.make_chunks(result)
        for _ in range(steps):
            result = self.simulate(result, 3, 4)
        return result

class Region:
    """ An abstract class of Region to contain tier and type.
    """
    def __init__(self, rtype, tier):
        self.rtype = rtype
        self.tier = tier

    @property
    def rtype(self):
        return self.__rtype

    @rtype.setter
    def rtype(self, rtype):
        self.__rtype = rtype

    @property
    def tier(self):
        return self.__tier

    @tier.setter
    def tier(self, tier):
        if not isinstance(tier, int):
            raise TypeError("tier must be integer")
        self.__tier = tier

    def populate(self, screen):
        pass

class LandRegion(Region):
    """ Land where the Player can move freely.
    """
    def __init__(self, tier, biome=""):
        super().__init__("land", tier)
        self.biome = biome

    @property
    def biome(self):
        return self.__biome

    @biome.setter
    def biome(self, biome):
        self.__biome = biome

class WaterRegion(Region):
    """ Water where Player is required to have a Raft before crossing.
    """
    def __init__(self, tier):
        super().__init__("water", tier)

class SpawnRegion(LandRegion):

    def __init__(self):
        super().__init__(0, "spawn")

class GrasslandRegion(LandRegion):

    def __init__(self):
        super().__init__(0, "grassland")

class ForestRegion(LandRegion):

    def __init__(self):
        super().__init__(1, "forest")

class PlateauRegion(LandRegion):

    def __init__(self):
        super().__init__(1, "plateau")

class JungleRegion(LandRegion):

    def __init__(self):
        super().__init__(2, "jungle")

class MountainsRegion(LandRegion):

    def __init__(self):
        super().__init__(2, "mountains")

class DesertRegion(LandRegion):

    def __init__(self):
        super().__init__(3, "desert")

class SnowRegion(LandRegion):

    def __init__(self):
        super().__init__(3, "snow")
