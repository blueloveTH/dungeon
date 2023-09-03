import random
from ..room import Room

class SizeCategory:
    # minDim, maxDim, roomValue
    NORMAL = (4, 10, 1)
    LARGE = (10, 14, 2)
    GIANT = (14, 18, 3)

    @staticmethod	
    def connection_weight(val):
        return val * val


class StandardRoom(Room):
    def __init__(self):
        super().__init__()
        self.sizeCat = None
        self.setSizeCat()
        
    def sizeCatProbs(self):
        return [1, 0, 0]
    
    def setSizeCat(self):
        return self.setSizeCat(0, len(SizeCategory) - 1)
    
    def setSizeCat(self, maxRoomValue):
        return self.setSizeCat(0, maxRoomValue - 1)
    
    def setSizeCat(self, minOrdinal, maxOrdinal):
        probs = self.sizeCatProbs()
        categories = list(SizeCategory)
        if len(probs) != len(categories):
            return False
        for i in range(minOrdinal):
            probs[i] = 0
        for i in range(maxOrdinal + 1, len(categories)):
            probs[i] = 0
        ordinal = random.choices(range(len(categories)), weights=probs)[0]
        if ordinal != -1:
            self.sizeCat = categories[ordinal]
            return True
        else:
            return False
    
    def minWidth(self):
        return self.sizeCat.minDim
    
    def maxWidth(self):
        return self.sizeCat.maxDim
    
    def minHeight(self):
        return self.sizeCat.minDim
    
    def maxHeight(self):
        return self.sizeCat.maxDim
    
    def canMerge(self, l, p, mergeTerrain):
        cell = l.pointToCell(self.pointInside(p, 1))
        return (Terrain.flags[l.map[cell]] & Terrain.SOLID) == 0
    
    @staticmethod
    def createRoom():
        return random.choice(rooms)()
