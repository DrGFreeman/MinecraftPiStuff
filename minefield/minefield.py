# -*- coding: utf-8 -*-
#
################################################################################
#
# Jeux MineField pour Minecraft Pi sur Raspberry Pi
#
#- Trouver et détruire le bloc d'or puis revenir à son point de départ (bloc de "Glowing Obsidian")
#- Éviter les mines en utilisant l'indicateur de proximité (échelle de leds sur GPIO)
#
################################################################################

import random
import time
import math

from mcpi.minecraft import Minecraft
from mcpi import block

from EchGPIO import EchBVJR
from Effets import explosion
from Pt3D import Pt3D

########################################
# Fonctions

# Fonction qui enlève de la liste de mines les mines situées a proximité d'un point donné
def popMines(mines, point, distance):
    minesProx = [] # Liste des index des mines à la position du point
    for i in range(len(mines)): # Pour toutes les mines,
        distMine = point.distAxes(mines[i], 5) # on calcule la distance entre le point et la mine.
        if distMine <= distance: # Si la mine est à proximité,
            minesProx.append(i) # on ajoute l'index de la mine à la liste
    if len(minesProx) > 0:
        for i in minesProx: # Pour toutes les mines à proximité du point
            mines.pop(i) # on enlève la mine de la liste
    print("   ", len(minesProx), " Mines éliminée(s)")
    return mines

########################################
# Réglages du jeu
# Ajuster ces paramètres pour contrôler le niveau de difficulté

# Seuils de distance pour affichage LED
distBleu = 16
distVert = 8
distJaune = 5
distRouge = 3

# Seuil de distance pour l'explosion des mines
distMort = 1 # Le joueur meurt si il se trouve à cette distance d'une mine

# Nombre de mines
nbMines = 200

# Étendue des mines +/-
etendueMines = 100

# Distance à l'objectif
objDist = 40

########################################
# Préparation du jeu

# Initialisation de l'objet Échelle de LED Bleu-Vert-Jaune-Rouge
ech = EchBVJR(distBleu, distVert, distJaune, distRouge)

# Connection avec Minecraft Pi
mc = Minecraft.create()

# On détermine la position de départ du joueur (base) aléatoirement
print("Définition du point de départ")
bBaseOK = False
while not bBaseOK:
    base = Pt3D(random.randint(-35, 35), 0, random.randint(-35, 35)) # On détermine une position aléatoire
    base.y = mc.getHeight(base.x, base.z) # On obtiens la hauteur du monde à la position "base"
    bBase = mc.getBlock(base.x, base.y - 1, base.z) # On obtiens le type de bloc sous la position "base"
    bBaseOK = True
    for id in [8, 9, 10, 11, 18]: # On vérifie que la base n'est pas sur l'eau, la lave ou un arbre
        if bBase == id:
            bBaseOK = False
print("   Point de départ défini")

# Génération aléatoire des mines
print("Génération des mines")
mines = [] # Liste des mines (objets Pt3D)
for mine in range(nbMines):
    mines.append(Pt3D(random.randint(-etendueMines, etendueMines) + base.x, -64, random.randint(-etendueMines, etendueMines) + base.z))

# On vérifie si il y a des mines à distance mortelle la position de départ
print("Vérification des mines à la position de départ")
print(len(mines))
mines = popMines(mines, base, distMort)
print(len(mines))

# Définition de l'objectif (position relative à la base)
print("Définition de l'objectif")
bObjOK = False
while not bObjOK: 
    objAzimut = random.uniform(-math.pi, math.pi) # Azimut de l'objectif déterminé au hasard (+/- Pi = +/- 180 deg.))
    obj = Pt3D(objDist * math.cos(objAzimut) + base.x, 0, objDist * math.sin(objAzimut) + base.z) # Pt3D correspondant à l'objectif
    obj.y = mc.getHeight(obj.x, obj.z) # On obtiens la hauteur du monde à l'objectif
    bObj = mc.getBlock(obj.x, obj.y - 1, obj.z) # On obtiens le type de bloc sous l'objectif
    bObjOK = True
    for id in [8, 9, 10, 11, 18]: # On vérifie que l'objectif n'est pas sur l'eau, la lave ou un arbre
        if bObj == id:
            bObjOK = False
print("   Objectif défini")

# On vérifie si il y a des mines à la position de l'objectif
print("Vérification des mines à l'objectif")
mines = popMines(mines, obj, distMort)


# Positionnement des blocs base, objectif et du joueur
mc.setBlock(base.x, base.y, base.z, block.GLOWING_OBSIDIAN) # On place un bloc rouge au point de départ
mc.player.setTilePos(base.x + 1, mc.getHeight(base.x + 1, base.z), base.z) # On place le joueur au point d edépart
mc.setBlock(obj.x, obj.y, obj.z, block.GOLD_BLOCK) # On place un bloc d'or à l'objectif

########################################
# Début du jeu

# Initialisation des variables d'état servant au contrôle du jeu
vivant = True # Le joueur est en vie?
objAtteint = False # L'objectif est atteint?
reussi = False # La mission est réussie?

# Instructions au joueur
mc.postToChat("Trouvez et detruisez le bloc d'or")
mc.postToChat("Attention aux mines..!")
mc.postToChat("Utilisez votre detecteur de mines")

print("Début du jeu")
ti = time.time() # Temps au début du jeu

try:
    while vivant and not reussi: # Boucle tant que le joueur est vivant et n'a pas réussi la mission
     
        p = mc.player.getTilePos() # Obtention de la position du joueur
        pos = Pt3D(p.x, p.y, p.z) # Assignation de la position dans un Pt3D
        
        # Calcul de la distance à la mine la plus proche
        distMin = 1000000. # On débute avec une distance min très grande
        for i in range(len(mines)): # Pour toutes les mines ...
            dist = pos.distAxes(mines[i], 5) # on calcule la distance entre le joueur et la mine
            if dist < distMin: # Si la distance est inférieur à la distance min...
                distMin = dist # on assigne la nouvelle distance min
                mineProx = mines[i] # On assigne le Pt3D de la mine la plus proche

        ech.onVal(distMin) # Affichage de la distance sur l'echelle LED
        if distMin <= 1: # Si le joueur se trouve sur une mine...
            vivant = False # le joueur est mort!

        if mc.getBlock(obj.x, obj.y, obj.z) == 0: # Si le bloc objectif est de l'air (détruit)
            if not objAtteint: # Si le joueur n'as pas encore atteint l'objectif
                mc.postToChat("Objectif atteint! Bravo!")
                mc.postToChat("Maintenant retournez a votre base (bloc rouge)")
                mc.postToChat("et detruisez le bloc")
            objAtteint = True

        if mc.getBlock(base.x, base.y, base.z) == 0: # Si le joueur détruit le bloc de la base
            if objAtteint: # Si l'objectif est déjà atteint
                reussi = True # Le joueur a réussi la mission
            else: # Sinon
                mc.postToChat("Vous devez d'abord trouver et detruite le bloc d'or")
                mc.setBlock(base.x, base.y, base.z, block.GLOWING_OBSIDIAN) # On remet le bloc à la base

    # Fin du jeu
    ech.buzzer.stop()
    if not vivant: # Cas où le joueur est mort
        explosion(mc, 3) # Explosion à la position du joueur
        mc.postToChat("BOUM!!!")
        mc.postToChat(" ")
        mc.postToChat("Oh oh... Vous etes mort(e)!")
        print("Le joueur est mort - Nettoyage")
        mc.setBlock(base.x, base.y, base.z, block.AIR) # On enlève le bloc à la base
        mc.setBlock(obj.x, obj.y, obj.z, block.AIR) # On enlève le bloc à l'objectif
        ech.blinkOnVal(0, 3) # Clignotement des LEDs
        time.sleep(6)
        ech.blinkOff()
    else: # Cas où le joueur a réussi la mission
        mc.postToChat("Felicitations, vous avez reussi!")
        ech.off() # Arrêt de l'échelle de LED
        # Calcul et affichage du temps de jeu
        tf = time.time() - ti
        minutes = str(int(tf // 60))
        secondes = str(int(tf % 60))
        mc.postToChat(("Temps: " + minutes + "m " + secondes + "s"))

except KeyboardInterrupt: # Si interruption
    print("Jeu interrompu - Nettoyage")
    mc.setBlock(base.x, base.y, base.z, block.AIR) # On enlève le bloc à la base
    mc.setBlock(obj.x, obj.y, obj.z, block.AIR) # On enlève le bloc à l'objectif


