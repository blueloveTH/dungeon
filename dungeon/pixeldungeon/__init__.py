import random, math
from dungeon.level import Level
from dungeon.algorithm import dijkstra, _NodeLike
from dungeon.base import Rect
from dungeon.debug import plot_rects

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
        elif (random.random() <= (self.min_size * self.min_size / rect.area()) and w <= self.max_size and h <= self.max_size) or w < self.min_size or h < self.min_size:
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


class RoomType:
    NULL = 0
    STANDARD = 1
    ENTRANCE = 2
    EXIT = 3
    BOSS_EXIT = 4
    TUNNEL = 5
    PASSAGE = 6
    SHOP = 7
    BLACKSMITH = 8
    TREASURY = 9
    ARMORY = 10
    LIBRARY = 11
    LABORATORY = 12
    VAULT = 13
    TRAPS = 14
    STORAGE = 15
    MAGIC_WELL = 16
    GARDEN = 17
    CRYPT = 18
    STATUE = 19
    POOL = 20
    RAT_KING = 21
    WEAK_FLOOR = 22
    PIT = 23
    ALTAR = 24


class Room:
    def __init__(self, rect: Rect):
        self.rect = rect
        self.neighbours = []
        self.connected = {}
        self.price = 1
        self.type = RoomType.NULL

    def width(self) -> int:
        return self.rect.width()
    
    def height(self) -> int:
        return self.rect.height()

    def get_neighbours(self) -> list[tuple[_NodeLike, int]]:
        return [(nb, nb.price) for nb in self.neighbours]
    
    def connect(self, other: 'Room') -> None:
        if other in self.connected:
            return
        self.connected[other] = None
        other.connected[self] = None

    def __lt__(self, other: 'Room') -> bool:
        return True


class PixelDungeonLevel(Level):
    def __init__(self, width=32, height=32):
        super(PixelDungeonLevel, self).__init__(width, height)
        self.rooms = None

    def get_greedy_path(self, dist: dict[Room, int], start: Room, end: Room) -> list[Room]:
        """从 `start` 到 `end` 的贪心路径"""
        path = [start]
        while path[-1] is not end:
            next = min(path[-1].neighbours, key=lambda nb: dist[nb])
            if next in path:
                break
            path.append(next)
        return path
    
    def plot_rooms_with_dist(self, dist: dict[Room, int], filename=None):
        labels, colors = [], []
        for room in self.rooms:
            labels.append(dist[room])
            colors.append(dist[room])
        plot_rects(
            [room.rect for room in self.rooms],
            self.width, self.height,
            filename=filename,
            labels=labels,
            colors=colors
        )

    def plot_room_path(self, path: list[Room], filename=None):
        dist = {}
        for room in self.rooms:
            dist[room] = 0
        for i, room in enumerate(path, start=1):
            dist[room] = i
        self.plot_rooms_with_dist(dist, filename=filename)

    def build(self) -> bool:
        # split the level into rooms
        rects = []
        splitter = _RectSplitter(7, 9)
        splitter.split(Rect(0, 0, self.width, self.height), rects)
        if len(rects) < 8:
            return False
        
        plot_rects(rects, self.width, self.height, filename='pd_01.png')
        
        self.rooms = [Room(rect) for rect in rects]
        del rects

        # connect the rooms by corridors
        for i in range(len(self.rooms) - 1):
            for j in range(i + 1, len(self.rooms)):
                room_i, room_j = self.rooms[i], self.rooms[j]
                rij = room_i.rect.intersect(room_j.rect)
                if (rij.width() == 0 and rij.height() >= 3) or (rij.height() == 0 and rij.width() >= 3):
                    room_i.neighbours.append(room_j)
                    room_j.neighbours.append(room_i)

        # determine the entrance and exit rooms
        dist = None
        min_distance = int(math.sqrt(len(self.rooms)))
        for _ in range(10):
            while True:
                room_entrance = random.choice(self.rooms)
                # make sure `room_entrance` is big enough
                if room_entrance.width() >= 4 and room_entrance.height() >= 4:
                    break
            while True:
                room_exit = random.choice(self.rooms)
                # make sure `room_exit` is big enough and not the same as `room_entrance`
                if room_exit is not room_entrance and room_exit.width() >= 4 and room_exit.height() >= 4:
                    break
            # make sure the distance between `room_entrance` and `room_exit` is big enough
            dist = dijkstra(self.rooms, room_exit)
            if dist[room_entrance] >= min_distance:
                self.plot_rooms_with_dist(dist, filename='pd_02.png')
                break
        else:
            # failed to find a suitable start and end room after 10 tries
            return False
        
        room_entrance.type = RoomType.ENTRANCE
        room_exit.type = RoomType.EXIT

        connected = set()
        connected.add(room_entrance)

        path = self.get_greedy_path(dist, room_entrance, room_exit)
        self.plot_room_path(path, filename='pd_03.png')

        for i in range(len(path) - 1):
            path[i].connect(path[i + 1])
            connected.add(path[i + 1])

        # reset the price of each room
        for room in path:
            room.price = dist[room]

        dist = dijkstra(self.rooms, room_exit)
        self.plot_rooms_with_dist(dist, filename='pd_04.png')

        path = self.get_greedy_path(dist, room_entrance, room_exit)
        self.plot_room_path(path, filename='pd_05.png')

        for i in range(len(path) - 1):
            path[i].connect(path[i + 1])
            connected.add(path[i + 1])

        n_connected = int(len(self.rooms) * random.uniform(0.5, 0.7))
        connected = list(connected)
        while len(connected) < n_connected:
            _0: Room = random.choice(connected)
            _1: Room = random.choice(_0.neighbours)
            if _1 not in connected:
                _0.connect(_1)
                connected.append(_1)

        self.plot_rooms_with_dist({
            room: 1 if room in connected else 0
            for room in self.rooms
        }, filename='pd_06.png')

        # assign room types
        specials = [
            RoomType.ARMORY, RoomType.WEAK_FLOOR, RoomType.MAGIC_WELL, RoomType.CRYPT, RoomType.POOL, RoomType.GARDEN, RoomType.LIBRARY,
            RoomType.TREASURY, RoomType.TRAPS, RoomType.STORAGE, RoomType.STATUE, RoomType.LABORATORY, RoomType.VAULT, RoomType.ALTAR
        ]
        special_rooms = 0
        for r in self.rooms:
            if r.type == RoomType.NULL and len(r.connected) == 1:
                if specials and r.width() > 3 and r.height() > 3 and random.randint(0, special_rooms * special_rooms + 2) == 0:
                    n = len(specials)
                    r.type = specials[min(random.randint(0, n), random.randint(0, n))]
                    specials.remove(r.type)
                    special_rooms += 1
                elif random.randint(0, 1) == 0:
                    neighbours = set()
                    for nb in r.neighbours:
                        if nb not in r.connected and nb.type not in specials and nb.type != RoomType.PIT:
                            neighbours.add(nb)
                    if len(neighbours) > 1:
                        r.connect(random.choice(list(neighbours)))

        count = 0
        for r in self.rooms:
            if r.type == RoomType.NULL:
                connections = len(r.connected)
                if connections == 0:
                    pass
                elif random.randint(0, connections * connections) == 0:
                    r.type = RoomType.STANDARD
                    count += 1
                else:
                    r.type = RoomType.TUNNEL

        # while count < 4:
        #     r = random.choice(self.rooms)
        #     if r.type == RoomType.TUNNEL:
        #         r.type = RoomType.STANDARD
        #         count += 1

		# paint();
		# paintWater();
		# paintGrass();
		
		# placeTraps();
                    
        return True
