
from arcana.prefab import Prefab, prefab_db
import random
import enum
import typing
from arcana.tilemap import TileMap
from arcana.npc import NPC

@enum.unique
class AreaStyle(enum.IntEnum):
    SCATTER = 0
    LINK = 1

class BorderStyle(enum.IntEnum):
    VOID = 0
    TERRAIN = 1
    WATER = 2

class Area():
    
    floor_tiles: dict[int, tuple]
    terrain_tiles: dict[int, tuple]
    flavor_tiles: dict[int, tuple]
    enemy_spawns: dict[int, tuple]
    prefabs: dict[int, Prefab]
    style: AreaStyle
    border_style: BorderStyle
    clutter_seed: int
    portals: list
    tilemap: TileMap
    spawn_count: int
    
    def __init__(self, dimensions: tuple):
        self.floor_tiles = dict()
        self.terrain_tiles = dict()
        self.flavor_tiles = dict()
        self.enemy_spawns = dict()
        self.prefabs = dict()
        self.portals = list()
        self.style = AreaStyle.SCATTER
        self.border_style = BorderStyle.VOID
        self.clutter_seed = 25
        self.tilemap = None
        self.dimensions = dimensions
        self.prefab_count = 0
        
        
    
    def gen_tilemap(self) -> TileMap:
        if self.tilemap:
            return self.tilemap
        else:
            tilemap = TileMap(self.dimensions)
            tilemap.carpet_tile_map(self.floor_tiles, self.prefab_count)
            tilemap.add_random_scenery(self.terrain_tiles, self.clutter_seed)
            tilemap.add_portals(self.portals)
            tilemap.add_prefab(self.prefabs)
            if self.border_style == BorderStyle.TERRAIN:
                tilemap.border_tile_map(self.terrain_tiles[list(self.terrain_tiles.keys())[0]])
            elif self.border_style == BorderStyle.VOID:
                tilemap.void_border()
            
            #tilemap.add_enemies(self.enemy_spawns, self.spawn_count)
            self.tilemap = tilemap
            return tilemap
    
#NPC Constructor(name, statpool (seed for statpool constructor), level, image (path to image as string), damage_range (as a tuple of min to max damage range))    
forest_floor_tiles = {65: ("grasstile.png",), 35: ("dirttile.png",)}
forest_terrain_tiles = {75: ("treetile.png", ("SOLID", "OPAQUE")), 15: ("bush.png", ("SOLID",)), 10: ("rock.png", ("SOLID",))}
forest_enemy_group = {36: {"name": "Goblin", "statpool": "goblin", "level": 1, "image": "goblin.png", "damage_range": (1, 5)}, 34: {"name": "Kobold", "statpool": "kobold", "level": 1, "image": "kobold.png", "damage_range": (2, 3)}, 20: {"name": "Wolf", "statpool": "wolf", "level": 1, "image": "wolf.png", "damage_range": (2, 5)}, 10: {"name": "Ogre", "statpool": "ogre", "level": 2, "image": "ogre.png", "damage_range": (3, 8)}}
forest_prefabs = {51: prefab_db["druid"], 49: prefab_db["tree_alley"]}

def make_test_area():
    area = Area((33, 13))
    area.floor_tiles = forest_floor_tiles
    area.terrain_tiles = forest_terrain_tiles
    area.border_style = BorderStyle.TERRAIN
    area.enemy_spawns = forest_enemy_group
    area.prefabs = forest_prefabs
    area.spawn_count = 6
    area.prefab_count = 6
    #protocol for adding portals:
    # List of tuples, each tuple covering a single portal
    # ( (Either Coordinates for the static location of the portal or a tuple of two coordinates for a range of random possible locations), (constructor arguments for the portal Scenery object))
    area.portals = [ ( ( (12, 7), ), ("doortile.png", list(), 0, "test2") ) ]
    return area

def make_second_test_area():
    area = Area((14, 9))
    area.floor_tiles = forest_floor_tiles
    area.terrain_tiles = forest_terrain_tiles
    area.border_style = BorderStyle.TERRAIN
    area.enemy_spawns = forest_enemy_group
    area.spawn_count = 9
    area.prefab_count = 2
    #protocol for adding portals:
    # List of tuples, each tuple covering a single portal
    # ( (Either Coordinates for the static location of the portal or a tuple of two coordinates for a range of random possible locations), (constructor arguments for the portal Scenery object))
    area.portals = [ ( ( (2, 2), (3, 6) ), ("doortile.png", list(), 0, "test") ) ]
    return area

area_db = {
    "test": make_test_area(),
    "test2": make_second_test_area(),
}
