from arcana.tile import *
from arcana.direction import *
from arcana.tilemap import TileMap

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
    
def test_valid_coord():
    
    testmap = TileMap((10, 10))
    assert not testmap.valid_coord((15, 5))
    assert testmap.valid_coord((3, 9))
    assert not testmap.valid_coord((-4, -3))

def test_border_tile():
    testmap = TileMap((10, 10))
    assert not testmap.is_border_tile(54)
    assert testmap.is_border_tile(6)
    assert testmap.is_border_tile(95)
    
def test_shortest_path():
    testmap = TileMap((10, 10))
    testmap.add_tile(Tile(), (0, 0))
    testmap.add_tile(Tile(), (1, 0))
    testmap.add_tile(Tile(), (2, 0))
    testmap.add_tile(Tile(), (3, 0))
    testmap.add_tile(Tile(), (4, 0))
    testmap.add_tile(Tile(), (1, 1))
    testmap.add_tile(Tile(), (2, 1))
    testmap.add_tile(Tile(), (3, 1))
    testmap.add_tile(Tile(), (4, 1))
    testmap.add_tile(Tile(), (0, 1))
    testmap.add_tile(Tile(), (0, 2))
    testmap.add_tile(Tile(), (1, 2))
    testmap.add_tile(Tile(), (2, 2))
    testmap.add_tile(Tile(), (3, 2))
    testmap.add_tile(Tile(), (4, 2))

    expected_path = [(0, 0), (1, 1), (2, 2), (3, 2), (4, 2)]    
    path = testmap.get_shortest_path(testmap.get_tile((0, 0)), testmap.get_tile((4, 2)))
    for i, tile in enumerate(path):
        assert tile.loc == expected_path[i]
    
def test_shortest_path_failure():
    testmap = TileMap((10, 10))
    testmap.add_tile(Tile(), (0, 0))
    testmap.add_tile(Tile(), (1, 0))
    testmap.add_tile(Tile(), (2, 0))
    testmap.add_tile(Tile(), (3, 0))
    testmap.add_tile(Tile(), (4, 0))
    testmap.add_tile(Tile(), (1, 1))
    testmap.add_tile(Tile(), (2, 1))
    testmap.add_tile(Tile(), (3, 1))
    testmap.add_tile(Tile(), (4, 1))
    testmap.add_tile(Tile(), (0, 1))
    
    testmap.add_tile(Tile(), (9, 9))
    
    path = testmap.get_shortest_path(testmap.get_tile((0, 0)), testmap.get_tile((9, 9)))
    assert path == []
    
