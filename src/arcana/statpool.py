import enum

@enum.unique
class Stat(enum.IntEnum):
    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2
    INTELLIGENCE = 3
    WISDOM = 4
    FLAT_DR = 5
    PERCENT_DR = 6
    DEFENCE = 7
    SPEED = 8
    ACCURACY = 9

class StatPool():

    def __init__(self, seed="default"):
        if seed=="default" or not seed in stat_seeds:
            self.stats = {
                Stat.STRENGTH : 10,
                Stat.DEXTERITY : 10,
                Stat.CONSTITUTION : 10,
                Stat.INTELLIGENCE: 10,
                Stat.WISDOM: 10,
                Stat.SPEED: 1.0,
                Stat.ACCURACY: 50,
                Stat.FLAT_DR: 0,
                Stat.PERCENT_DR: 0,
                Stat.DEFENCE: 0
            }


stat_seeds = {
    "default": {
                Stat.STRENGTH : 10,
                Stat.DEXTERITY : 10,
                Stat.CONSTITUTION : 10,
                Stat.INTELLIGENCE: 10,
                Stat.WISDOM: 10,
                Stat.SPEED: 1.0,
                Stat.ACCURACY: 50,
                Stat.FLAT_DR: 0,
                Stat.PERCENT_DR: 0,
                Stat.DEFENCE: 0
            }
        
}