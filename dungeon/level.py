"""
一个 Level 对应一个地图，地图分为两层，地形层和物品层。

地形层 list[int]：用于存储地形的连通信息，如墙壁、地板、水等。
物品层 dict[object]：用于存储物品信息，如宝箱、门、怪物等。
"""

class Level:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.reset()

    def reset(self) -> None:
        self.terrain = [0] * (self.width * self.height)
        self.items = [None] * (self.width * self.height)
        self._visited = [False] * (self.width * self.height)
    
    def generate(self):
        # repeatedly build until success
        while not self.build():
            self.reset()

    # virtual methods
    def build(self) -> bool:
        raise NotImplementedError
