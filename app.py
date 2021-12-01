from window import Game, TestScreen, TestScreen2
import time

game = Game()
""" scr = TestScreen()
scr2 = TestScreen2()
game.change_screen(scr)
time.sleep(1)
game.change_screen(scr2)
time.sleep(1)
game.change_screen(scr) """

while True:
    game.tick()