import random
from dungeon.level import Level
from dungeon.algorithm import Rect

class _RectSplitter:
    def __init__(self, min_size: int, max_size: int):
        self.min_size = min_size
        self.max_size = max_size

    def split(self, rect: Rect, output: list[Rect]) -> None:
        w = rect.width()
        h = rect.height()

        if w > self.max_size and h < self.min_size:
            vw = random.randint(rect.left + 3, rect.right - 3)
            self.split(Rect(rect.left, rect.top, vw, rect.bottom), output)
            self.split(Rect(vw, rect.top, rect.right, rect.bottom), output)
        elif h > self.max_size and w < self.min_size:
            vh = random.randint(rect.top + 3, rect.bottom - 3)
            self.split(Rect(rect.left, rect.top, rect.right, vh), output)
            self.split(Rect(rect.left, vh, rect.right, rect.bottom), output)
        elif (random.random() <= (self.min_size * self.min_size / rect.square()) and w <= self.max_size and h <= self.max_size) or w < self.min_size or h < self.min_size:
            output.append(Rect(rect.left, rect.top, rect.right, rect.bottom))
        else:
            if random.random() < (w - 2) / (w + h - 4):
                vw = random.randint(rect.left + 3, rect.right - 3)
                self.split(Rect(rect.left, rect.top, vw, rect.bottom), output)
                self.split(Rect(vw, rect.top, rect.right, rect.bottom), output)
            else:
                vh = random.randint(rect.top + 3, rect.bottom - 3)
                self.split(Rect(rect.left, rect.top, rect.right, vh), output)
                self.split(Rect(rect.left, vh, rect.right, rect.bottom), output)

class Room:
    def __init__(self, rect: Rect):
        self.rect = rect
        self.neighbours = []

class PixelDungeonLevel(Level):
    """生成 Pixel Dungeon 地图的算法"""

    def __init__(self, width: int, height: int):
        super(PixelDungeonLevel, self).__init__(width, height)
        self.rooms = None

    def build(self) -> bool:
        # split the level into rooms
        rects = []
        splitter = _RectSplitter(7, 9)
        splitter.split(Rect(0, 0, self.width - 1, self.height - 1), rects)
        if len(rects) < 8:
            return False
        
        self.rooms = [Room(rect) for rect in rects]

        # connect the rooms (not sure about this)
        for i in range(len(self.rooms) - 1):
            for j in range(i + 1, len(self.rooms)):
                self.rooms[i].neighbours.append(self.rooms[j])
            