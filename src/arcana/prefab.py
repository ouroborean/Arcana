from arcana.tile import Tile
from arcana.tilemap import TileMap

class Prefab(TileMap):
    
    
    
    def __init__(self, dimensions):
        super().__init__(dimensions)
    
        
scen_tree=("treetile.png", ("SOLID", "OPAQUE"))
tile_grass=("grasstile.png",)
tile_dirt=("dirttile.png",)

def make_druid_circle():
    prefab = Prefab((5, 5))
    