# -*- coding: utf-8 -*-

class Pt3D:
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return (self.x, self.y, self.z)

    def dist3D(self, pt):
        return ((self.x - pt.x)**2 + (self.y - pt.y)**2 + (self.z - pt.z)**2)**.5

    def distAxes(self, pt, axes):
        dx = 0
        dy = 0
        dz = 0
        if axes % 2 != 0:
            dx = self.x - pt.x
        if axes > 3:
            dz = self.z - pt.z
        if axes in [2, 3] or axes in [6, 7]:
            dy = self.y - pt.y
        return (dx**2 + dy**2 + dz**2)**.5

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**.5
