from arcana.npc import NPC
from arcana.tile_status import TileStatus


class Enemy(NPC):
    
    
    def __init__(self, name="Fred", statpool="default", level=1, image="rogueplayer.png", damage_range=(1, 3)):
        super().__init__(name, statpool, level, image, damage_range)
        
        self.actions = {
            TileStatus.HOSTILE : self.npc_swap,
            TileStatus.BLOCKED : self.npc_stand,
            TileStatus.ALLIED : self.npc_attack,
            TileStatus.EMPTY : self.npc_move,
            TileStatus.PLAYER : self.npc_attack
        }
        