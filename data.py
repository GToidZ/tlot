from datetime import datetime as dt

class GameData:
    
    def __init__(self, filename="game.save"):
        self.filename = filename
        self.magic = b"\x01\x4b\x55\x02"
        self.sep = b"\x5c"

    def save(self, player, world):
        with open(self.filename, "wb") as f:
            f.write(self.magic)
            dtnow = dt.now()
            dtstring = dtnow.strftime("%Y%m%d%H%M%S")
            f.write(bytes.fromhex(dtstring))
            seed = ''.join(hex(ord(x))[2:] for x in world.seed)
            f.write(bytes.fromhex(seed))
            f.write(self.sep)
            
            name = ''.join(hex(ord(x))[2:] for x in player.name)
            bname = bytes.fromhex(name)
            if len(bname) < 16:
                bname += b'\x00' * (16 - len(bname))
            f.write(bname)
            x = str(player.region[0])
            y = str(player.region[1])
            f.write(bytes.fromhex("0" + x if len(x) <= 1 else x))
            f.write(bytes.fromhex("0" + x if len(y) <= 1 else y))
            # TODO: Continue from Score