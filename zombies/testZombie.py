import math
import time
from mcpi.minecraft import Minecraft
from numpy import random

from Pt3D import Pt3D
from SuperBlock import SuperBlock
from Zombie import Attraction
from Zombie import Zombie
from Zombie import ZombieGroup
  

zone = 100
nbZombies = 120

zombies = ZombieGroup()
zombies.addZombies(nbZombies, -zone, -zone, zone, zone)

ax = []
az = []

mc = Minecraft.create()
pos = mc.player.getTilePos()

plAttr = Attraction(1, 4, pos.x, pos.y, pos.z)


superBlocks = []

for z in range(zombies.getNbZmb()):
    superBlocks.append(SuperBlock(mc, zombies.zombies[z].getPosObj(), 35, 1))

zombies.addAttr(plAttr)
dt = .2

attrs = []

try:
    vivant = True
    while vivant:

        pos = mc.player.getTilePos()
        plAttr.setPos(pos.x, 0, pos.z)
        
        t0 = time.time()

        zombies.update(dt)

        for zb in range(len(zombies.zombies)):
            if plAttr.pos.distAxes(zombies.zombies[zb].getPosObj(),  5) < 40:
                superBlocks[zb].show()
                superBlocks[zb].move()
            else:
                superBlocks[zb].hide()

        for hit in mc.events.pollBlockHits():
            blockData = mc.getBlockWithData(hit.pos.x, hit.pos.y, hit.pos.z)
            if blockData.id == 35 and blockData.data == 1:
                sbHits = []
                for sb in range(len(superBlocks)):
                    hitDist = superBlocks[sb].currPos.dist3D(Pt3D(hit.pos.x, hit.pos.y, hit.pos.z))
                    if  hitDist < 1:
                        sbHits.append(sb)
                if len(sbHits) > 0:   
                    for sb in sbHits:
                        superBlocks[sb].delete()
                        superBlocks.pop(sb)
                        zombies.delete(sb)
                    print("zombies remaining: ", zombies.getNbZmb())
            elif blockData.id == 50 or blockData.id == 51:
                attrs.append(Attraction(2, 10, hit.pos.x, hit.pos.y, hit.pos.z))
                attrs[len(attrs) - 1].type = 'PONCTUAL'
                attrs[len(attrs) - 1].timeCst = 30
                print("test")
                for zombie in zombies.zombies:
                    zombie.addAttr(attrs[len(attrs) - 1])
                                   
        for sb in range(len(superBlocks)):
            if superBlocks[sb].currPos.distAxes(plAttr.pos, 5) <= 1:
                mc.postToChat("!Oh no! ... you have been bitten!")
                vivant = False

        dt = time.time() - t0

        print(dt)
        if dt < .2:
            time.sleep(.2 - dt)

    time.sleep(5)
    for sb in range(len(superBlocks)):
        superBlocks[sb].delete()

except KeyboardInterrupt:
    print("\nKeyboardInterrupt - killing all zombies!")
    for sb in range(len(superBlocks)):
        superBlocks[sb].delete()
