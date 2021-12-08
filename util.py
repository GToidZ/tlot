import random
import turtle
import cartography as car
import entities as ent
import window as win
import data
import string

valid_x = [x*32 for x in range(2, 23)]
valid_y = [x*32 for x in range(2, 19)]

def update_region(root, player, world):
    """ Fires when the player goes into a new region,
    the map updates and the screen re-renders with
    a new map.
    """
    for e in root.entities:
        if isinstance(e, ent.Enemy) and e.isvisible():
            player.score -= (e.tier + 1) * 100
            if player.score <= 0:
                player.score = 0
    player.hp = 5
    scr = win.PlayingScreen(root, player, world)
    root.change_screen(scr)
    x, y = player.region[0], player.region[1]
    if [x, y] in world.itemmap.values():
        item = [k for k,v in world.itemmap.items() if v == [x, y]]
        scr.add_entity(ent.ItemEntity(world.get_prng().choice(valid_x),
                                      world.get_prng().choice(valid_y),
                                      item[0]))
        world.itemmap[item[0]] = 0
    if [x, y] != world.spawnpoint:
        for _ in range(random.randint(2, 5)):
            scr.add_entity(ent.Enemy(world.get_prng().choice(valid_x),
                                    world.get_prng().choice(valid_y),
                                    world.get_tiermap()[x][y], root))

def new_game(root):
    """ The new game event, takes player name as input
    and creates a new world with random seed.
    """
    name = turtle.textinput("TLoT",
                            "Enter a player name (ASCII, max 16 chars):")
    if not name:
        return False
    while True:
        if len(name) > 16 or len(name) <= 0 or \
            any((c not in string.printable) for c in name):
                name = turtle.textinput("Try again.",
                            "Enter a player name (ASCII, max 16 chars):")
                if not name:
                    return False
        else:
            break

    root.save = "game.save"
    world = car.GameWorld()
    player = ent.Player(name, world)
    update_region(root, player, world)
    return True

def load_game(root):
    """ The load game event, if "game.save" is not found it takes
    another file with ".save" extension instead. Then, it
    regenerates the world and loads player data.
    """
    try:
        open("game.save", "rb")
        dat = data.GameData()
        root.save = "game.save"
    except IOError:
        filename = turtle.textinput("TLoT", "Enter a TLoT .save filename:")
        if not filename:
            return False
        try:
            open(filename + ".save", "rb")
            dat = data.GameData(filename + ".save")
            root.save = filename + ".save"
        except IOError:
            return False
    player, world = dat.load()
    update_region(root, player, world)
    return True

def save_game(root, player, world):
    """ The save game event, creates a new save file.
    """
    dt = data.GameData(root.save)
    dt.save(player, world)
    turtle.bye()

def game_over(root, player):
    """ The medium method for calling the game over screen.
    """
    scr = win.GameOverScreen(root, player)
    root.change_screen(scr)