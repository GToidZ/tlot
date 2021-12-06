import window, items
from cartography import GameWorld
from entities import Player
import time

game = window.Game()
world = GameWorld()
player = Player("Test", world)
world.ascii_map()
juice = items.LemonJuice()
raft = items.Raft()
player.inventory.add(juice)
player.inventory.add(raft)
fsc = window.MenuScreen(game)
scr = window.PlayingScreen(game, player)
game.change_screen(fsc)
time.sleep(3)
game.change_screen(scr)

while True:
    game.tick()
