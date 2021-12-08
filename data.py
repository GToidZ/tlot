from datetime import datetime as dt
import entities as ent
import cartography as car
import items as its

class GameData:
    """ A class to save/load game data as a custom 79~ bytes file.
    """
    def __init__(self, filename="game.save"):
        self.filename = filename
        self.magic = b"\x01\x4b\x55\x02"
        self.sep = b"\x5c"

    def save(self, player, world):
        """ Saving function.
        """
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
            f.write(bytes.fromhex("0" + y if len(y) <= 1 else y))
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
                    x = str(region[0])
                    y = str(region[1])
                    if len(x) < 2:
                        x = "0" + x
                    if len(y) < 2:
                        y = "0" + y
                    f.write(bytes.fromhex(x))
                    f.write(bytes.fromhex(y))
                    f.write(bytes.fromhex(item.key))

    def load(self):
        """ Loading function. Returns Player and GameWorld.
        """
        with open(self.filename, "rb") as f:
            if f.read(4) != self.magic:
                raise IOError("File is not a save file")
            f.seek(7, 1)
            seed = f.read(20)

            wld = car.GameWorld(seed.decode("ascii"))
            wld.itemmap = {}
            IP = its.InvincibilityPot()
            LJ = its.LemonJuice()
            BA = its.BowArrow()
            CJ = its.CannedJellyfish()
            RAFT = its.Raft()
            wld.itemmap[IP] = 0
            wld.itemmap[LJ] = 0
            wld.itemmap[BA] = 0
            wld.itemmap[CJ] = 0
            wld.itemmap[RAFT] = 0

            f.seek(1, 1)

            name = f.read(16)
            name = name.replace(b'\x00', b'')

            player = ent.Player(name.decode("ascii"), wld)

            posx = (f.read(1)).hex()
            posy = (f.read(1)).hex()

            truex = int(posx)
            truey = int(posy)
            if truex < 0 or truex > 23:
                raise IOError(f"Unknown x position: {posx}")
            if truey < 0 or truey > 23:
                raise IOError(f"Unknown y position: {posy}")

            player.region = [truex, truey]

            rscore = f.read(5)
            rscore = [rscore[i:i+1] for i in range(len(rscore))]
            ns = []
            for n in rscore:
                n = n.hex()
                if n[0] != "0":
                    raise IOError(f"Unknown score index: {n}")
                n = n[1:]
                ns.insert(0, n)
            score = int(''.join(ns))
            player.score = score

            tier = int((f.read(1)).hex())
            if tier > 3:
                raise IOError(f"Unknown tier: {tier}")
            player.tier = tier
            
            f.seek(1, 1)
            
            bswim = f.read(1)
            if bswim not in [b'\x00', b'\xFF']:
                raise IOError(f"Unknown bool operation: {bswim}")
            if bswim == b'\xFF':
                player.can_swim = True
                player.inventory.add(RAFT)
            else:
                player.can_swim = False
            
            f.seek(1, 1)
            
            items = f.read(4)
            items = [items[i:i+1] for i in range(len(items))]
            for i in items:
                if i == b'\xA0':
                    player.inventory.add(IP)
                if i == b'\xA1':
                    player.inventory.add(LJ)
                if i == b'\xA2':
                    player.inventory.add(BA)
                if i == b'\xA3':
                    player.inventory.add(CJ)
            
            f.seek(1, 1)
            
            while True:
                item = f.read(3)
                struct = [item[i:i+1] for i in range(len(item))]
                if "" in struct or len(struct) != 3:
                    break
                x = int(struct[0].hex())
                y = int(struct[1].hex())
                key = struct[2]
                if key == b'\xA0':
                    wld.itemmap[IP] = [x, y]
                if key == b'\xA1':
                    wld.itemmap[LJ] = [x, y]
                if key == b'\xA2':
                    wld.itemmap[BA] = [x, y]
                if key == b'\xA3':
                    wld.itemmap[CJ] = [x, y]
                if key == b'\xFF':
                    wld.itemmap[RAFT] = [x, y]

        return player, wld