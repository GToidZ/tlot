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
            score = str(player.score)[::-1]
            ns = ""
            if len(score) < 5:
                score += '0' * (5 - len(score))
            for i in score:
                i = "0" + i
                ns += i
            bscore = bytes.fromhex(ns)
            f.write(bscore)
            f.write(bytes.fromhex("0" + str(player.tier)))
            f.write(self.sep)

            if player.can_swim:
                swim = b'\xff'
            else:
                swim = b'\x00'
            f.write(swim)
            f.write(self.sep)

            items = ""
            for i in player.inventory.active:
                items += i.key
            bitems = bytes.fromhex(items)
            if len(bitems) < 4:
                bitems += b'\x00' * (4 - len(bitems))
            f.write(bitems)
            f.write(self.sep)

            items = ""
            for i in world.itemmap:
                if world.itemmap[i] != 0:
                    item = i
                    region = world.itemmap[i]
                    f.write(bytes.fromhex(item.key))
                    x = str(region[0])
                    y = str(region[1])
                    if len(x) < 2:
                        x = "0" + x
                    if len(y) < 2:
                        y = "0" + y
                    f.write(bytes.fromhex(x))
                    f.write(bytes.fromhex(y))
                    