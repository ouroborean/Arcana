
from arcana.actor import Actor
from arcana.statpool import Stat, StatPool
from arcana.tile import TileStatus
from arcana.equipment import Equipment
import enum
import random
from arcana.direction import pos_to_direction

class NPCDamage(enum.IntEnum):
    MAX = 0
    MIN = 1

class NPC(Actor):
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])

    def __init__(self, name="Fred", statpool="default", level=1, image="rogueplayer.png", damage_range=(1, 3)):
        super().__init__()
        self.player = False
        self.statpool = StatPool(statpool)
        self.current_health = self.max_health
        self.item_drop = Equipment()
        self.level = level
        self.name = name
        self.character_class = ""
        self.image = image
        self.can_act = True
        self.can_move = True
        self.target_tile_loc = ()
        self.turn_counter = 0
        self.damage = {
            NPCDamage.MAX : damage_range[1],
            NPCDamage.MIN : damage_range[0]
        }

    @property
    def max_health(self):
        return 50 + (3 * (self.statpool.stats[Stat.CONSTITUTION] - 10))

    @property
    def speed(self):
        return self.statpool.stats[Stat.SPEED]
    
    @property
    def accuracy(self):
        return self.statpool.stats[Stat.ACCURACY]
    
    @property
    def flat_dr(self):
        return self.statpool.stats[Stat.FLAT_DR]
    
    @property
    def percent_dr(self):
        return self.statpool.stats[Stat.PERCENT_DR]
    
    @property
    def defence(self):
        return self.statpool.stats[Stat.DEFENCE]

    def change_health(self, damage):
        self.current_health -= damage

    def npc_think(self, tile):
        player_adj = self.check_adjacent_tiles(tile)
        if player_adj == False:
            self.npc_wander(tile)

    def get_random_direction(self):
        random_dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)])
        if not random_dir == (0,0):
            return random_dir
        else:
            self.get_random_direction()


    def npc_wander(self, tile_start):
        chosen_tile = tile_start.neighbor[pos_to_direction[self.get_random_direction()]]
        if chosen_tile.status != TileStatus.BLOCKED:
            self.check_npc_bump(chosen_tile, tile_start)
        else:
            self.npc_wander(tile_start)

        

    def check_npc_bump(self, tile_target, tile_start):
        self.actions[tile_target.status](tile_target, tile_start)
        
    def check_adjacent_tiles(self, tile):
        for adj_tile in tile.neighbor.values():
            if adj_tile:
                if adj_tile.status == TileStatus.PLAYER:
                    self.check_npc_bump(adj_tile, tile)
                    return True
        return False
                

    def npc_attack(self, target, tile):
        print(f"{self.name} attacking {target.actor.name}") 
        self.do_npc_combat(target.actor)   

    def get_damage_done(self, target):
        self.damage_done = (random.randint(self.damage[NPCDamage.MIN],self.damage[NPCDamage.MAX]) - target.flat_dr) * (1 - target.percent_dr)
        return self.damage_done

    def combat_roll(self, target):
        attack_roll = random.randint(1, self.accuracy)
        return attack_roll >= target.defence

    def combat_miss(self):
        print(self.name + " missed!")

    def do_npc_combat(self, target):
        if self.can_act:
            if self.combat_roll(target):
                print(f"The {self.name}'s attack hit!")
                damage = self.get_damage_done(target)
                print(f"The {self.name} did {damage} damage!")
                target.change_health(damage)
                print(f"{target.name} has {target.current_health} health left!")
            else:
                self.combat_miss()
        self.is_new = True

    def npc_swap(self, tile_target, tile_start):
        pass

    def npc_stand(self, tile_target, tile_start):
        pass

    def npc_move(self, tile_target, tile_start):
        tile_target.actor = self
        tile_target.actor.is_new = True
        diff = (tile_target.loc[0] - self.loc[0], tile_target.loc[1] - self.loc[1])
        self.loc = self + diff
        tile_start.actor = None