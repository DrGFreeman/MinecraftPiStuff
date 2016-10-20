# -*- coding: utf-8 -*-
from gpiozero import LED
import threading
import time


class EchBVJR:

    def __init__(self, sB, sV, sJ, sR):
        self.sB = sB
        self.sV = sV
        self.sJ = sJ
        self.sR = sR
        self.b = False
        self.v = False
        self.j = False
        self.r = False
        self.ledB = LED(17) # LED bleue sur pin 17
        self.ledV = LED(27) # LED verte sur pin 27
        self.ledJ = LED(22) # LED jaune sur pin 22
        self.ledR = LED(16) # LED rouge sur pin 16

    def onVal(self, val):
        if val <= self.sB:
            self.b = True
        else:
            self.b = False
        if val <= self.sV:
            self.v = True
        else:
            self.v = False
        if val <= self.sJ:
            self.j = True
        else:
            self.j = False
        if val <= self.sR:
            self.r = True
        else:
            self.r = False
        self.appliquer()

    def off(self):
        self.b = False
        self.v = False
        self.j = False
        self.r = False
        self.appliquer()

    def blinkVal(self, val, freq): # Clignotement de l'echelle
        self.blink = True
        ti = time.time()
        while self.blink:
            self.onVal(val)
##            print(self.etat())
            time.sleep(1 / freq / 2)
            self.off()
##            print(self.etat())
            time.sleep(1 / freq / 2)
                
    def blinkOnVal(self, val, freq): # Demarrage du clignotement
        thread1 = threading.Thread(target = self.blinkVal, args = (val, freq))
        thread1.start()

    def blinkOff(self): # Fin du clignotement
        self.blink = False

    def appliquer(self): # Application de l'etat choisi aux LEDs
        if self.b:
            self.ledB.on()
        else:
            self.ledB.off()
        if self.v:
            self.ledV.on()
        else:
            self.ledV.off()
        if self.j:
            self.ledJ.on()
        else:
            self.ledJ.off()
        if self.r:
            self.ledR.on()
        else:
            self.ledR.off()
            
    def etat(self): # Methode de test pour rapporter l'état de chaque led dans le terminal
        aff = ""
        if self.b:
            aff += "B"
        if self.v:
            aff += "V"
        if self.j:
            aff += "J"
        if self.r:
            aff += "R"
        return aff
