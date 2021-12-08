import window as win

""" Run this file to get started.
"""

game = win.Game()
fsc = win.MenuScreen(game)
game.change_screen(fsc)

while True:
    game.tick()
