from collections import OrderedDict
from random import randint
from dungeon.base import Rect

class Room(Rect):
    def __init__(self, other=None):
        super().__init__(other)
        self.neighbours = []
        self.connected = OrderedDict()
        self.distance = 0
        self.price = 1
    
    def set(self, other):
        super().set(other)
        for r in other.neighbours:
            self.neighbours.append(r)
            r.neighbours.remove(other)
            r.neighbours.append(self)
        for r, d in other.connected.items():
            r.connected.pop(other)
            r.connected[self] = d
            self.connected[r] = d
        return self
    
    def minWidth(self):
        return -1
    
    def maxWidth(self):
        return -1
    
    def minHeight(self):
        return -1
    
    def maxHeight(self):
        return -1
    
    def setSize(self):
        return self.setSize(self.minWidth(), self.maxWidth(), self.minHeight(), self.maxHeight())
    
    def forceSize(self, w, h):
        return self.setSize(w, w, h, h)
    
    def setSizeWithLimit(self, w, h):
        if w < self.minWidth() or h < self.minHeight():
            return False
        else:
            self.setSize()
            if self.width() > w or self.height() > h:
                self.resize(min(self.width(), w) - 1, min(self.height(), h) - 1)
            return True
    
    def setSize(self, minW, maxW, minH, maxH):
        if minW < self.minWidth() or maxW > self.maxWidth() or minH < self.minHeight() or maxH > self.maxHeight() or minW > maxW or minH > maxH:
            return False
        else:
            self.resize(randint(minW, maxW) - 1, randint(minH, maxH) - 1)
            return True
    
    def pointInside(self, from, n):
        step = Point(from)
        if from.x == self.left:
            step.offset(n, 0)
        elif from.x == self.right:
            step.offset(-n, 0)
        elif from.y == self.top:
            step.offset(0, n)
        elif from.y == self.bottom:
            step.offset(0, -n)
        return step
    
    def width(self):
        return super().width() + 1
    
    def height(self):
        return super().height() + 1
    
    def random(self, m=1):
        return Point(randint(self.left + m, self.right - m), randint(self.top + m, self.bottom - m))
    
    def inside(self, p):
        return p.x > self.left and p.y > self.top and p.x < self.right and p.y < self.bottom
    
    def center(self):
        return Point((self.left + self.right) // 2 + (1 if (self.right - self.left) % 2 == 1 else 0), (self.top + self.bottom) // 2 + (1 if (self.bottom - self.top) % 2 == 1 else 0))
    
    ALL = 0
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    
    def minConnections(self, direction):
        return 1 if direction == self.ALL else 0
    
    def curConnections(self, direction):
        if direction == self.ALL:
            return len(self.connected)
        else:
            total = 0
            for r, d in self.connected.items():
                i = self.intersect(r)
                if direction == self.LEFT and i.width() == 0 and i.left == self.left:
                    total += 1
                elif direction == self.TOP and i.height() == 0 and i.top == self.top:
                    total += 1
                elif direction == self.RIGHT and i.width() == 0 and i.right == self.right:
                    total += 1
                elif direction == self.BOTTOM and i.height() == 0 and i.bottom == self.bottom:
                    total += 1
            return total
    
    def remConnections(self, direction):
        return 0 if self.curConnections(self.ALL) >= self.maxConnections(self.ALL) else self.maxConnections(direction) - self.curConnections(direction)
    
    def maxConnections(self, direction):
        return 16 if direction == self.ALL else 4
    
    def canConnect(self, p):
        return (p.x == self.left or p.x == self.right) != (p.y == self.top or p.y == self.bottom)
    
    def canConnect(self, direction):
        return self.remConnections(direction) > 0
    
    def canConnect(self, r):
        i = self.intersect(r)
        foundPoint = False
        for p in i.getPoints():
            if self.canConnect(p) and r.canConnect(p):
                foundPoint = True
                break
        if not foundPoint:
            return False
        if i.width() == 0 and i.left == self.left:
            return self.canConnect(self.LEFT) and r.canConnect(self.RIGHT)
        elif i.height() == 0 and i.top == self.top:
            return self.canConnect(self.TOP) and r.canConnect(self.BOTTOM)
        elif i.width() == 0 and i.right == self.right:
            return self.canConnect(self.RIGHT) and r.canConnect(self.LEFT)
        elif i.height() == 0 and i.bottom == self.bottom:
            return self.canConnect(self.BOTTOM) and r.canConnect(self.TOP)
        else:
            return False
    
    def canMerge(self, l, p, mergeTerrain):
        return False
    
    def merge(self, l, other, merge, mergeTerrain):
        Painter.fill(l, merge, mergeTerrain)
    
    def addNeighbour(self, other):
        if other in self.neighbours:
            return True
        i = self.intersect(other)
        if (i.width() == 0 and i.height() >= 2) or (i.height() == 0 and i.width() >= 2):
            self.neighbours.append(other)
            other.neighbours.append(self)
            return True
        return False
    
    def connect(self, room):
        if (room in self.neighbours or self.addNeighbour(room)) and room not in self.connected and self.canConnect(room):
            self.connected[room] = None
            room.connected[self] = None
            return True
        return False
    
    def clearConnections(self):
        for r in self.neighbours:
            r.neighbours.remove(self)
        self.neighbours.clear()
        for r in self.connected:
            r.connected.remove(self)
        self.connected.clear()
    
    def paint(self, level):
        pass
    
    def canPlaceWater(self, p):
        return True
    
    def waterPlaceablePoints(self):
        points = []
        for i in range(self.left, self.right + 1):
            for j in range(self.top, self.bottom + 1):
                p = Point(i, j)
                if self.canPlaceWater(p):
                    points.append(p)
        return points
    
    def canPlaceGrass(self, p):
        return True
    
    def grassPlaceablePoints(self):
        points = []
        for i in range(self.left, self.right + 1):
            for j in range(self.top, self.bottom + 1):
                p = Point(i, j)
                if self.canPlaceGrass(p):
                    points.append(p)
        return points
    
    def canPlaceTrap(self, p):
        return True
    
    def trapPlaceablePoints(self):
        points = []
        for i in range(self.left, self.right + 1):
            for j in range(self.top, self.bottom + 1):
                p = Point(i, j)
                if self.canPlaceTrap(p):
                    points.append(p)
        return points
    
    def canPlaceItem(self, p, l):
        return self.inside(p)
    
    def itemPlaceablePoints(self, l):
        points = []
        for i in range(self.left, self.right + 1):
            for j in range(self.top, self.bottom + 1):
                p = Point(i, j)
                if self.canPlaceItem(p, l):
                    points.append(p)
        return points
    
    def canPlaceCharacter(self, p, l):
        return self.inside(p)
    
    def charPlaceablePoints(self, l):
        points = []
        for i in range(self.left, self.right + 1):
            for j in range(self.top, self.bottom + 1):
                p = Point(i, j)
                if self.canPlaceCharacter(p, l):
                    points.append(p)
        return points
    
    def distance(self):
        return self.distance
    
    def setDistance(self, value):
        self.distance = value
    
    def price(self):
        return self.price
    
    def setPrice(self, value):
        self.price = value
    
    def edges(self):
        edges = []
        for r, d in self.connected.items():
            if d.type == Door.Type.EMPTY or d.type == Door.Type.TUNNEL or d.type == Door.Type.UNLOCKED or d.type == Door.Type.REGULAR:
                edges.append(r)
        return edges
    
    def onLevelLoad(self, level):
        pass
    
class Door(Point):
    def __init__(self, p=None):
        super().__init__(p)
        self.type = Door.Type.EMPTY
    
    def set(self, type):
        if type > self.type:
            self.type = type
    
    def storeInBundle(self, bundle):
        bundle.put("x", self.x)
        bundle.put("y", self.y)
        bundle.put("type", self.type)
    
    def restoreFromBundle(self, bundle):
        self.x = bundle.getInt("x")
        self.y = bundle.getInt("y")
        self.type = bundle.getEnum("type", Door.Type)
