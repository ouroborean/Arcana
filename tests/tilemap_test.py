from arcana.tile import *
from arcana.tilemap import *
from arcana.direction import *
from arcana.prefab import *

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
    
def test_add_tile_in_line():
    
    tilemap = TileMap((10, 10))
    tilemap.add_tiles_in_line(tile_grass, (0, 0), Direction.EAST, 5)
    
    for i in range(5):
        assert tilemap.get_tile((i, 0))
    assert not tilemap.get_tile((5, 0))
        
    tilemap.add_tiles_in_line(tile_grass, (4, 7), Direction.SOUTH, 10)
    
    for i in range(3):
        assert tilemap.get_tile((4, i + 7))
        
def test_add_scenery_in_line():
    
    tilemap = TileMap((10, 10))
    tilemap.add_tiles_in_line(tile_grass, (0, 0), Direction.EAST, 5)
    
    tilemap.add_scenery_in_line(scen_tree, (2, 0), Direction.EAST, 2)
    
    assert not tilemap.get_tile((1, 0)).scenery
    assert tilemap.get_tile((3, 0)).scenery
    assert not tilemap.get_tile((4, 0)).scenery