import window, items
from entities import Player

game = window.Game()
player = Player("Test")
potion = items.InvisibilityPot()
player.inventory.add(potion)
scr = window.PlayingScreen(player)
game.change_screen(scr)

while True:
    game.tick()