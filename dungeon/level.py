"""
一个 Level 对应一个地图，地图分为两层，地形层和物品层。

地形层 list[int]：用于存储地形的连通信息，如墙壁、地板、水等。
物品层 dict[object]：用于存储物品信息，如宝箱、门、怪物等。
"""

import random

class Level:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.reset()

    def reset(self) -> None:
        self.terrain = [0] * (self.width * self.height)
        self.items = [None] * (self.width * self.height)
    
    def generate(self, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)
        # repeatedly build until success
        while not self.step_build():
            self.reset()

		# buildFlagMaps();
		# cleanWalls();
		
		# createMobs();
		# createItems();

    # virtual methods
    def step_build(self) -> bool:
        """
        1. 先确定这个关卡要有几个房间，先生成房间集（并不连接）
        2. 50%概率使用LoopBuilder，50%概率使用FigureEightBuilder
        """
        raise NotImplementedError
