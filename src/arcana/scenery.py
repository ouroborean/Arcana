import enum
from typing import Tuple
import sdl2.ext

@enum.unique
class SceneryStatus(enum.IntEnum):
    WALKABLE = 0
    OPAQUE = 1
    SOLID = 2
    INVIOLABLE = 3

class Scenery():
    
    status: set
    loc: Tuple[int, int]
    sprite: sdl2.ext.SoftwareSprite
    
    def __init__(self, image, status:list[str] = list()):
        self.images = image
        self.status = set()
        self.loc = (0, 0)
        self.sprite = None
        for scenerystatus in status:
            self.status.add(SceneryStatus[scenerystatus])
    
class Portal(Scenery):
    
    area_dest: str
    portal_id: int
    locked: bool
    
    def __init__(self, image, status:list[str], portal_id: int=0, area_dest: str=""):
        super().__init__(image, status)
        self.portal_id = portal_id
        self.area_dest = area_dest
        self.status.add(SceneryStatus.WALKABLE)
        self.locked = False
        self.sprite = None
        
    def lock_location(self, loc):
        self.loc = loc    
        