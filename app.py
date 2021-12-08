import window as win
import time

game = win.Game()
fsc = win.MenuScreen(game)
game.change_screen(fsc)

while True:
    game.tick()
