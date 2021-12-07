import window as win

def update_region(root, player, world):
    scr = win.PlayingScreen(root, player, world)
    root.change_screen(scr)