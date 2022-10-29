import enum

@enum.unique
class Direction(enum.IntEnum):
    NORTH     = 0
    EAST      = 1
    SOUTH     = 2
    WEST      = 3
    NORTHWEST = 4
    NORTHEAST = 5
    SOUTHWEST = 6
    SOUTHEAST = 7

counters = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
    Direction.NORTHWEST: Direction.SOUTHEAST,
    Direction.SOUTHEAST: Direction.NORTHWEST,
    Direction.NORTHEAST: Direction.SOUTHWEST,
    Direction.SOUTHWEST: Direction.NORTHEAST
}

pos_to_direction = {
    (0, -1): Direction.NORTH,
    (0, 1): Direction.SOUTH,
    (1, 0): Direction.EAST,
    (-1, 0): Direction.WEST,
    (1, 1): Direction.SOUTHEAST,
    (-1, 1): Direction.SOUTHWEST,
    (1, -1): Direction.NORTHEAST,
    (-1, -1): Direction.NORTHWEST
}

direction_to_pos = {
    Direction.NORTH: (0, -1) ,
    Direction.SOUTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTHWEST: (-1, 1),
    Direction.NORTHEAST: (1, -1),
    Direction.NORTHWEST: (-1, -1)
}

def counter_direction(direction) -> Direction:
    return counters[direction]

def offset_to_direction(pos_offset) -> Direction:
    return pos_to_direction[pos_offset]

def direction_to_offset(direction) -> Direction:
    return direction_to_pos[direction]