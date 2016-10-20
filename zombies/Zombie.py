# -*- coding: utf-8 -*-

import math
import numpy.random as random
import threading
import time
from Pt3D import Pt3D

class Zombie:

##  Separer la methode move selon les differents modes.
##  Ajouter une methode move pour attraction de groupe avec aspect aleatoire

    def __init__(self, id, x = 0, y = 0, z = 0):
        self.id = id
        self.pos = Pt3D(x, y, z) # implement check of mc height block type to ensure is on ground
        self.dir = (random.random() - .5) * 2 * math.pi # Input direction in x, z plane, from x to z in radians
        self.speed = random.normal(.15, .05)
        self.mode = 'RANDOM'
        self.attrs = []
        self.attrThr = .1 #.05
    
    def setPos(self, x, y, z): # Set position from x, y, z coordinates
        self.pos.setPos(x, y, z)

    def getPos(self): # Get position in x, y, z coordinates
        return self.pos.getPos()

    def setPosObj(self, pt): # Set position from a Pt3D object
        self.pos = pt
    
    def getPosObj(self):
        return self.pos

    def setDir(self, angle):
        self.dir = angle

    def setDirXZ(self, x, z):
        self.setDir(math.atan2(z, x))

    def getDir(self):
        return self.dir

    def getDirXZ(self):
        return math.cos(self.getDir()), math.sin(self.getDir())
    
    def chgDir(self, angle):
        self.dir = math.atan2(math.sin(self.dir + angle), math.cos(self.dir + angle))

    def setSpeed(self, speed):
        if speed <= 0:
            self.speed = 0
        elif speed >= 1:
            self.speed = 1
        else:
            self.speed = speed

    def getSpeed(self):
        return self.speed

    def getSpeedXZ(self):
        return self.getSpeed() * math.cos(self.getDir()), self.getSpeed() * math.sin(self.getDir())

    def chgSpeedRatio(self, ratio):
        self.setSpeed(self.speed * (1 + ratio))

    def chgSpeed(self, incr):
        self.setSpeed(self.speed + incr)

    def addAttr(self, attr):
        self.attrs.append(attr)

    def remAttr(self, attr):
        if len(self.attrs) > 0:
            for i in range(len(self.attrs)):
                if self.attrs[i].id == attr.id:
                    attrId = i
            self.attrs.pop(attrId)

    def move(self, timeStep):
        if len(self.attrs) > 0:
            maxStr = -1
            for attr in self.attrs:
                dist = self.pos.dist3D(attr.getPosObj())
                attrStr = attr.getStr(dist)
                if  attrStr > maxStr:
                    mainAttr = attr
                    attrDist = dist
                    maxStr = attrStr
                elif attr.type == 'PONCTUAL':
                    self.remAttr(attr)
##                    print("Ponctual attraction overriden, removing attraction")
            attrStr = mainAttr.getStr(attrDist)
##            print("Attration strength: ", attrStr)

            if attrStr >= self.attrThr:
                self.mode == 'FOLLOW'
                dx = self.pos.dir3D(mainAttr.getPosObj())[0]
                dz = self.pos.dir3D(mainAttr.getPosObj())[2]
                self.setDirXZ(dx, dz)
##                print("Zombie ", self.id, "follows attraction ", mainAttr.id)
                self.setSpeed(1. * attrStr)
            else:
                if mainAttr.type == 'PONCTUAL':
                    self.remAttr(mainAttr)
##                    print("Attraction too weak for zombie ", self.id, ", removing attraction")
                self.mode = 'RANDOM'

        if self.mode == 'RANDOM':
            self.chgSpeedRatio(random.normal(0, .15)) # minor change in speed
            if random.random() < .08: # Add random chance of greaterspeed change
                self.chgSpeed(random.normal(0, .3))
##                print("Speed Change")
            self.chgDir(random.normal(0, math.pi / 8 * (1.5 - self.speed))) # reduce dir change for higher speeds
            # implement obstacle avoidance - checking if world height - current y is > 2 (cannot move)
        self.pos.x += self.speed * math.cos(self.dir) * timeStep
        # implement minecraft.getHeight for y coord (check if on ground)
        self.pos.z += self.speed * math.sin(self.dir) * timeStep


class Attraction:

    def __init__(self, id, strength, x = 0, y = 0, z = 0):
        self.id = id
        self.type = 'CONT_MOVING'
        self.pos = Pt3D(x, y, z)
        self.initT = time.time()
        self.initStr = strength
        self.timeCst = 15
        self.distCst = 15
        self.distThr = 20
        self.str = strength
        self.srcPos = Pt3D(x, y, z)

    def setSrcPos(self, src):
        self.srcPos = src

    def followSrc(self):
        self.pos = self.srcPos

    def getStr(self, dist): # rearrange so that ponctual does not increase as distance reduces.
        thrFact = 1.
        timeFact = 1.
        if dist > self.distThr:
            thrFact = 0.
        if self.type == 'PONCTUAL':
            timeFact = math.exp((self.initT - time.time()) / self.timeCst)
        return self.str * thrFact * timeFact * math.exp(-dist / self.distCst)

    def getPos(self):
        if self.type == 'CONT_MOVING':
            self.followSrc()
        return self.pos.x, self.pos.y, self.pos.z

    def getPosObj(self):
        if self.type == 'CONT_MOVING':
            self.followSrc()
        return self.pos

    def setPos(self, x, y, z):
        self.pos.x, self.pos.y, self.pos.z = x, y, z
        
class ZombieGroup:

    def __init__(self):
        self.zombies = []

    def addZombies(self, nbZombies, xMin, zMin, xMax, zMax):
        for i in range(nbZombies):
            x = random.randint(xMin, xMax)
            z = random.randint(zMin, zMax)
            self.zombies.append(Zombie(i, x, 0, z))

    def addAttr(self, attraction):
        if len(self.zombies) > 0:
            for zombie in self.zombies:
                zombie.addAttr(attraction)

    def getNbZmb(self):
        return len(self.zombies)

    def update(self, timeStep):
        for zombie in self.zombies:
            zombie.move(timeStep)

    def delete(self, index):
        self.zombies.pop(index)
