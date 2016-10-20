from mcpi import block
from Pt3D import Pt3D

class SuperBlock:

    def __init__(self, mc, pt, bId, bData):
        self.currPos = Pt3D(int(pt.x), int(pt.y) + 1, int(pt.z))
        self.srcPos = pt
        self.id = bId
        self.data = bData
        self.display = False
        self.mc = mc
        self.mc.setBlock(pt.x, pt.y, pt.z, bId, bData)
        self.mc.setBlock(pt.x, pt.y - 1, pt.z, 35, 8)
        

    def move(self):
        if self.display:
            new = Pt3D(int(self.srcPos.x), 0, int(self.srcPos.z))
            dist = self.currPos.distAxes(new, 5)
            if dist >= 1:
                self.delete()
                new.y = self.mc.getHeight(new.x, new.z) + 1
                self.currPos.setPos(new.x, new.y, new.z)
                self.show()

    def delete(self):
        self.mc.setBlock(self.currPos.x, self.currPos.y, self.currPos.z, 0)
        self.mc.setBlock(self.currPos.x, self.currPos.y - 1, self.currPos.z, 0)

    def show(self):
        self.mc.setBlock(self.currPos.x, self.currPos.y, self.currPos.z, self.id, self.data)
        self.mc.setBlock(self.currPos.x, self.currPos.y - 1, self.currPos.z, 35, 8)
        self.display = True

    def hide(self):
        self.display = False
        self.delete()
        
