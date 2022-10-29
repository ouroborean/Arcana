from arcana.direction import Direction, counter_direction
import sdl2.ext

from typing import Tuple, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from arcana.scenery import Scenery

@enum.unique
class TileStatus(enum.IntEnum):
    EMPTY = 0
    HOSTILE = 1
    ALLIED = 2
    BLOCKED = 3


class Tile():
    
    loc: Tuple[int, int]
    neighbor: dict[Direction, "Tile"]
    #actor: "Actor"
    #game_objects: list["GameObject"]
    scenery: "Scenery"
    image_path: str
    g_cost: int
    h_cost: int
    path_parent: "Tile"
    sprite: sdl2.ext.SoftwareSprite
    hover_lens: sdl2.ext.SoftwareSprite
    hostile_lens: sdl2.ext.SoftwareSprite
    range_lens: sdl2.ext.SoftwareSprite
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])
    
    def __init__(self, image_path: str = ""):
        self.image_path = image_path
        self.sprite = None
        self.hover_lens = None
        self.range_lens = None
        self.hostile_lens = None
        self.g_cost = 0
        self.h_cost = 0
        self.neighbor = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None,
            Direction.SOUTHEAST: None,
            Direction.NORTHEAST: None,
            Direction.NORTHWEST: None,
            Direction.SOUTHWEST: None
        }
        self.actor = None
        self.game_objects = list()
        self.scenery = None
        self.path_parent = None
        
    @property
    def x(self) -> int:
        return self.loc[0]
    
    @property
    def y(self) -> int:
        return self.loc[1]
    
    @property
    def status(self) -> TileStatus:
        """Returns the status of the tile, as it relates to the allegiance of the actors on it, and the status of any terrain or scenery it might contain."""
        #TODO check for allied, enemy, or player status of actor, if one exists
        
        if self.scenery and not 0 in self.scenery.status:
            return TileStatus.BLOCKED
        else:
            return TileStatus.EMPTY
    
    def set_g_cost(self, cost):
        """The cumulative pathing value of the tile along the path the A* algorithm is currently walking. Will self adjust to catch changes in the shortest path, for erroneous circuitous pathing."""
        self.g_cost = cost
        
    def set_h_cost(self, tile):
        """The static distance from the tile to the destination tile in the current path-finding run. Ignores terrain."""
        self.h_cost = self.distance_to_tile(tile)
    
    @property
    def f_cost(self) -> int:
        """The total pathing value of the tile in relation to a designated start and end tile. Used in the A* pathing algorithm from TileMap's 'get_shortest_path'."""
        return self.g_cost + self.h_cost
    
    def distance_to_tile(self, tile):
        """Returns the overall distance to the targeted tile using a distance value of 10 for NSEW directions and 14 for the diagonal halfsies"""
        
        x_diff = abs(self.x - tile.x)
        y_diff = abs(self.y - tile.y)
        return (min(x_diff, y_diff) * 14) + (abs(x_diff - y_diff) * 10)
    
    def walkable(self, pedestrian):
        """Checks the state of the tile and the state of the Actor attempting to enter it and returns a boolean value defining whether or not they can."""
        #TODO check values of the pedestrian Actor for allegiance and affects like insubstantial...ness
        if self.status == TileStatus.BLOCKED:
            output = False
        elif self.status == TileStatus.EMPTY:
            output = True
        return output
    
    def set_loc(self, location):
        self.loc = location
    
    def add_game_object(self, obj):
        self.game_objects.append(obj)
    
    def remove_game_object(self, obj):
        self.game_objects.remove(obj)
        
    def apply_scenery(self, scenery):
        self.scenery = scenery
    
    def remove_scenery(self):
        self.scenery = None
    
    def add_actor(self, actor):
        self.actor = actor
        
    def remove_actor(self):
        self.actor = None
        
    def set_neighbor(self, direction, tile):
        self.neighbor[direction] = tile
        tile.neighbor[counter_direction(direction)] = self