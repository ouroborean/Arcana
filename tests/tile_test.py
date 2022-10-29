from arcana.tile import *
from arcana.direction import *

def test_distance_to_tile():
    
    tile1 = Tile()
    tile1.set_loc((2, 4))
    tile2 = Tile()
    tile2.set_loc((5, 5))
    
    assert tile1.distance_to_tile(tile2) == 34

def test_set_neighbor():
    
    tile1 = Tile()
    tile1.set_loc((2, 4))
    tile2 = Tile()
    tile2.set_loc((5, 5))
    
    tile1.set_neighbor(Direction.NORTHWEST, tile2)
    
    assert tile2.neighbor[Direction.SOUTHEAST] == tile1
