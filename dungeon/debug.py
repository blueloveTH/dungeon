import matplotlib.pyplot as plt
import numpy as np
from dungeon.base import Rect

def ascii_map_to_data(map) -> np.ndarray:
    data = [list(line) for line in map.strip().split('\n')]
    return np.array(data, dtype=np.int32)

def plot(data: np.ndarray | str, cmap=None, filename=None, no_show=False):
    if isinstance(data, str):
        data = ascii_map_to_data(data)
    cmap = cmap or plt.cm.get_cmap('tab20')
    plt.pcolor(data, cmap=cmap, edgecolors='k', linewidths=0.1)
    # plt.xticks(np.arange(0.5, data.shape[1]+0.5), range(data.shape[1]))
    # plt.yticks(np.arange(0.5, data.shape[0]+0.5), range(data.shape[0]))
    # tick per 5 units
    plt.xticks(np.arange(0, data.shape[1]+1, 5))
    plt.yticks(np.arange(0, data.shape[0]+1, 5))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()

    # for y in range(data.shape[0]):
    #     for x in range(data.shape[1]):
    #         plt.text(x+0.5, y+0.5, data[y, x], ha='center', va='center', fontsize=16)

    if filename:
        plt.savefig(filename)
    else:
        if not no_show:
            plt.show()

def plot_rects(rects: list[Rect], width: int, height: int, colors=None, labels=None, filename=None):
    plt.clf()
    if colors is not None:
        assert len(colors) == len(rects)
    if labels is not None:
        assert len(labels) == len(rects)
    data = np.zeros((height, width), dtype=np.int32)
    for index, rect in enumerate(rects):
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                if colors is None:
                    data[y, x] = index + 1
                else:
                    data[y, x] = colors[index]

    plot(data, no_show=True)

    # plot the rect borders
    for rect in rects:
        plt.plot([rect.left, rect.right, rect.right, rect.left, rect.left], [rect.top, rect.top, rect.bottom, rect.bottom, rect.top], 'k-', linewidth=0.5)

    if labels:
        for index, rect in enumerate(rects):
            center_x = (rect.left + rect.right) / 2
            center_y = (rect.top + rect.bottom) / 2
            plt.text(center_x, center_y, labels[index], ha='center', va='center', fontsize=16)

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    