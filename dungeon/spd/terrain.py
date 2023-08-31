class Terrain:
    CHASM = 0
    EMPTY = 1
    GRASS = 2
    EMPTY_WELL = 3
    WALL = 4
    DOOR = 5
    OPEN_DOOR = 6
    ENTRANCE = 7
    EXIT = 8
    EMBERS = 9
    LOCKED_DOOR = 10
    CRYSTAL_DOOR = 31
    PEDESTAL = 11
    WALL_DECO = 12
    BARRICADE = 13
    EMPTY_SP = 14
    HIGH_GRASS = 15
    FURROWED_GRASS = 30
    SECRET_DOOR = 16
    SECRET_TRAP = 17
    TRAP = 18
    INACTIVE_TRAP = 19
    EMPTY_DECO = 20
    LOCKED_EXIT = 21
    UNLOCKED_EXIT = 22
    SIGN = 23
    WELL = 24
    STATUE = 25
    STATUE_SP = 26
    BOOKSHELF = 27
    ALCHEMY = 28
    WATER = 29
    PASSABLE = 0x01
    LOS_BLOCKING = 0x02
    FLAMABLE = 0x04
    SECRET = 0x08
    SOLID = 0x10
    AVOID = 0x20
    LIQUID = 0x40
    PIT = 0x80

    flags = [0] * 256
    flags[CHASM] = AVOID | PIT
    flags[EMPTY] = PASSABLE
    flags[GRASS] = PASSABLE | FLAMABLE
    flags[EMPTY_WELL] = PASSABLE
    flags[WATER] = PASSABLE | LIQUID
    flags[WALL] = LOS_BLOCKING | SOLID
    flags[DOOR] = PASSABLE | LOS_BLOCKING | FLAMABLE | SOLID
    flags[OPEN_DOOR] = PASSABLE | FLAMABLE
    flags[ENTRANCE] = PASSABLE
    flags[EXIT] = PASSABLE
    flags[EMBERS] = PASSABLE
    flags[LOCKED_DOOR] = LOS_BLOCKING | SOLID
    flags[CRYSTAL_DOOR] = SOLID
    flags[PEDESTAL] = PASSABLE
    flags[WALL_DECO] = flags[WALL]
    flags[BARRICADE] = FLAMABLE | SOLID | LOS_BLOCKING
    flags[EMPTY_SP] = flags[EMPTY]
    flags[HIGH_GRASS] = PASSABLE | LOS_BLOCKING | FLAMABLE
    flags[FURROWED_GRASS] = flags[HIGH_GRASS]
    flags[SECRET_DOOR] = flags[WALL] | SECRET
    flags[SECRET_TRAP] = flags[EMPTY] | SECRET
    flags[TRAP] = AVOID
    flags[INACTIVE_TRAP] = flags[EMPTY]
    flags[EMPTY_DECO] = flags[EMPTY]
    flags[LOCKED_EXIT] = SOLID
    flags[UNLOCKED_EXIT] = PASSABLE
    flags[SIGN] = SOLID
    flags[WELL] = AVOID
    flags[STATUE] = SOLID
    flags[STATUE_SP] = flags[STATUE]
    flags[BOOKSHELF] = flags[BARRICADE]
    flags[ALCHEMY] = SOLID

    @staticmethod
    def discover(terr):
        if terr == Terrain.SECRET_DOOR:
            return Terrain.DOOR
        elif terr == Terrain.SECRET_TRAP:
            return Terrain.TRAP
        else:
            return terr

    @staticmethod
    def convertTilesFrom0_6_0b(map):
        for i in range(len(map)):
            if map[i] == 23:
                map[i] = 1
        return map
