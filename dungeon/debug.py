import matplotlib.pyplot as plt
import numpy as np
from dungeon.base import Rect

def ascii_map_to_data(map) -> np.ndarray:
    data = [list(line) for line in map.strip().split('\n')]
    return np.array(data, dtype=np.int32)

def plot(data: np.ndarray | str, cmap=None):
    if isinstance(data, str):
        data = ascii_map_to_data(data)
    cmap = cmap or plt.cm.get_cmap('tab20')
    plt.pcolor(data, cmap=cmap, edgecolors='k', linewidths=0.5)
    plt.xticks(np.arange(0.5, data.shape[1]+0.5), range(data.shape[1]))
    plt.yticks(np.arange(0.5, data.shape[0]+0.5), range(data.shape[0]))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x+0.5, y+0.5, data[y, x], ha='center', va='center', fontsize=16)

    plt.show()

def plot_rects(rects: list[Rect], width: int, height: int):
    data = np.zeros((height, width), dtype=np.int32)
    for index, rect in enumerate(rects):
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                data[y, x] = index + 1
    plot(data)