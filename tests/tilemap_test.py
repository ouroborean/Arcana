from arcana.tile import *
from arcana.tilemap import *
from arcana.direction import *

def test_add_tile():
    tile = Tile()
    tilemap = TileMap((10, 10))
    tilemap.add_tile(tile, (0, 0))
    
    assert tilemap.get_tile((0, 0))
    assert not tilemap.get_tile((5, 5))

def test_add_adjacent_tile():
    tile = Tile()
    tilemap = TileMap((10, 10))
    tilemap.add_tile(tile, (0, 0))
    tilemap.add_adjacent_tile(tile, Tile(), Direction.SOUTHEAST)
    
    assert tile.neighbor[Direction.SOUTHEAST]
    
    tilemap.add_adjacent_tile(tile, Tile(), Direction.NORTHWEST)
    
    assert not tile.neighbor[Direction.NORTHWEST]