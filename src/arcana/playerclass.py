import enum
from shikkoku.color import *

@enum.unique
class PlayerClass(enum.IntEnum):
    NONE = 0
    WARRIOR = 1
    WIZARD = 2
    ROGUE = 3
    CLERIC = 4
    
class_primary_colors = {
    PlayerClass.WARRIOR: RED,
    PlayerClass.WIZARD: BLUE,
    PlayerClass.ROGUE: GREEN,
    PlayerClass.CLERIC: YELLOW
    }

class_secondary_colors = {
    PlayerClass.WARRIOR: DARK_RED,
    PlayerClass.WIZARD: DARK_BLUE,
    PlayerClass.ROGUE: DARK_GREEN,
    PlayerClass.CLERIC: YELLOW
}
