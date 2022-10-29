from arcana.direction import *


def test_direction_reversal():
    
    assert counter_direction(Direction.NORTH) == Direction.SOUTH
    assert counter_direction(Direction.SOUTHEAST) == Direction.NORTHWEST
    assert counter_direction(counter_direction(Direction.NORTH)) == Direction.NORTH

def test_get_offset_from_direction():
    
    assert offset_to_direction((0, 1)) == Direction.SOUTH
    assert offset_to_direction((-1, -1)) == Direction.NORTHWEST
    assert offset_to_direction((-1, 0)) == Direction.WEST
    
def test_get_direction_from_offset():
    
    assert direction_to_offset(Direction.NORTHEAST) == (1, -1)
    assert direction_to_offset(counter_direction(Direction.SOUTH)) == (0, -1)
    assert direction_to_offset(offset_to_direction((-1, -1))) == ((-1, -1))
