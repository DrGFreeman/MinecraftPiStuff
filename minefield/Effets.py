# -*- coding: utf-8 -*-
from mcpi.minecraft import Minecraft
from mcpi import block
import random


def explosion(mc, dim):
    p = mc.player.getTilePos()
    d3 = dim
    d2 = d3 - 1
    d1 = d2 - 1

    mc.setBlocks(p.x - d2, p.y - d1, p.z - d1, p.x + d2, p.y + d1, p.z + d1, block.AIR)
    mc.setBlocks(p.x - d1, p.y - d1, p.z - d2, p.x + d1, p.y + d1, p.z + d2, block.AIR)
    mc.setBlocks(p.x - d1, p.y - d2, p.z - d1, p.x + d1, p.y + d2, p.z + d1, block.AIR)

    for i in range(-d3, d3):
        for j in range(-d3, d3):
            rand1 = random.randint(0, 4)
            rand2 = random.randint(0, 1)
            if rand1 > 0:
                if rand2 > 0:
                    mc.setBlock(p.x + i, p.y + d3, p.z + j, block.GRAVEL)
                else:
                    mc.setBlock(p.x + i, p.y + d3, p.z + j, block.SAND)
