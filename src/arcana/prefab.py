from arcana.tile import Tile
from arcana.direction import Direction
from arcana.tilemap import TileMap
from arcana.scenery import Scenery
from typing import Tuple

class Prefab(TileMap):
    
    entrance_loc: Tuple[int, int]
    name: str
    
    def __init__(self, dimensions):
        super().__init__(dimensions)
    
        
scen_tree=("treetile.png", ("SOLID", "OPAQUE"))
tile_grass=("grasstile.png",)
tile_dirt=("dirttile.png",)
circle_nw=("druid_circle_nw.png", ("WALKABLE",))
circle_ne=("druid_circle_ne.png", ("WALKABLE",))
circle_n=("druid_circle_n.png", ("WALKABLE",))
circle_w=("druid_circle_w.png", ("WALKABLE",))
circle_e=("druid_circle_e.png", ("WALKABLE",))
circle_s=("druid_circle_s.png", ("WALKABLE",))
circle_se=("druid_circle_se.png", ("WALKABLE",))
circle_sw=("druid_circle_sw.png", ("WALKABLE",))

def make_druid_circle():
    prefab = Prefab((5, 5))
    prefab.entrance_loc = (2, 0)
    prefab.name = "druid_circle"
    prefab.add_tiles_in_line(tile_grass, (1, 0), Direction.EAST, 3)
    prefab.add_tiles_in_line(tile_grass, (4, 1), Direction.SOUTH, 3)
    prefab.add_tiles_in_line(tile_grass, (3, 4), Direction.WEST, 3)
    prefab.add_tiles_in_line(tile_grass, (0, 3), Direction.NORTH, 3)
    prefab.add_tiles_in_line(tile_dirt, (1, 1), Direction.SOUTH, 3)
    prefab.add_tiles_in_line(tile_dirt, (2, 1), Direction.SOUTH, 3)
    prefab.add_tiles_in_line(tile_dirt, (3, 1), Direction.SOUTH, 3)
    prefab.add_scenery(Scenery(*scen_tree), prefab.get_tile((1, 0)))
    prefab.add_scenery(Scenery(*scen_tree), prefab.get_tile((3, 0)))
    prefab.add_scenery_in_line(scen_tree, (4, 1), Direction.SOUTH, 3)
    prefab.add_scenery_in_line(scen_tree, (3, 4), Direction.WEST, 3)
    prefab.add_scenery_in_line(scen_tree, (0, 3), Direction.NORTH, 3)
    prefab.add_scenery(Scenery(*circle_nw), prefab.get_tile((1, 1)))
    prefab.add_scenery(Scenery(*circle_ne), prefab.get_tile((3, 1)))
    prefab.add_scenery(Scenery(*circle_n), prefab.get_tile((2, 1)))
    prefab.add_scenery(Scenery(*circle_w), prefab.get_tile((1, 2)))
    prefab.add_scenery(Scenery(*circle_e), prefab.get_tile((3, 2)))
    prefab.add_scenery(Scenery(*circle_s), prefab.get_tile((2, 3)))
    prefab.add_scenery(Scenery(*circle_sw), prefab.get_tile((1, 3)))
    prefab.add_scenery(Scenery(*circle_se), prefab.get_tile((3, 3)))
    
    return prefab

def make_tree_alley():
    prefab = Prefab((7, 3))
    prefab.entrance_loc = (0, 1)
    prefab.name = "tree_alley"
    prefab.add_tiles_in_line(tile_grass, (0, 0), Direction.EAST, 7)
    prefab.add_tiles_in_line(tile_grass, (0, 1), Direction.EAST, 7)
    prefab.add_tiles_in_line(tile_grass, (0, 2), Direction.EAST, 7)
    prefab.add_scenery_in_line(scen_tree, (0, 0), Direction.EAST, 7)
    prefab.add_scenery_in_line(scen_tree, (0, 2), Direction.EAST, 7)
    
    return prefab

def make_tree_arena():
    prefab = Prefab((9, 9))
    prefab.entrance_loc = (0, 4)
    prefab.name = "tree_arena"
    for i in range(9):
        prefab.add_tiles_in_line(tile_grass, (0, i), Direction.EAST, 9)
    prefab.add_scenery_in_line(scen_tree, (0, 0), Direction.EAST, 9)
    prefab.add_scenery_in_line(scen_tree, (0, 8), Direction.EAST, 9)
    prefab.add_scenery_in_line(scen_tree, (8, 1), Direction.SOUTH, 7)
    prefab.add_scenery_in_line(scen_tree, (0, 1), Direction.SOUTH, 3)
    prefab.add_scenery_in_line(scen_tree, (0, 5), Direction.SOUTH, 3)
    
    return prefab

prefab_db = {
    "druid": make_druid_circle,
    "tree_alley": make_tree_alley,
    "tree_arena": make_tree_arena
}
    
    