import random
import turtle
import cartography as car
import entities as ent
import window as win
import string

valid_x = [x*32 for x in range(2, 23)]
valid_y = [x*32 for x in range(2, 19)]

def update_region(root, player, world):
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

    world = car.GameWorld()
    player = ent.Player(name, world)
    update_region(root, player, world)
    return True

def load_game(root):
    try:
        open("game.save", "rb")
    except IOError:
        filename = turtle.textinput("TLoT", "Enter a TLoT .save filename:")
        if not filename:
            return False
        try:
            open(filename + ".save", "rb")
        except IOError:
            return False

def game_over(root, player, world):
    scr = win.GameOverScreen(root)
    root.change_screen(scr)