from arcana.item import Item
import enum
import random

@enum.unique
class Slot(enum.IntEnum):
    HEAD = 0
    SHOULDERS = 1
    CHEST = 2
    HANDS = 3
    LEGS = 4
    FEET = 5

class Material(enum.IntEnum):
    CLOTH = 0
    LEATHER = 1
    METAL = 2

class Rarity(enum.IntEnum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3

class Stat(enum.IntEnum):
    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2
    INTELLIGENCE = 3
    WISDOM = 4
    FLAT_DR = 5
    PERCENT_DR = 6
    DEFENCE = 7



class Equipment(Item):

    def __init__(self, equip_slot = None, equip_material = None, equip_rarity = None):
        
        self.sprite = None
        self.equip_slot : Slot = equip_slot
        self.equip_material : Material = equip_material
        self.equip_rarity : Rarity = equip_rarity
        self.name = ""
        self.image = ""
        self.stat_changes = {}
        self.stat_range = {
            Rarity.COMMON : (1, 2),
            Rarity.UNCOMMON : (2, 4),
            Rarity.RARE : (6, 8),
            Rarity.EPIC : (10, 15)
        }
        self.material_name = {
            Material.CLOTH : "Cloth",
            Material.LEATHER : "Leather",
            Material.METAL : "Iron"
        }

        self.cloth_material_image = {
            Slot.HEAD : "cloth_head.png",
            Slot.SHOULDERS : "cloth_shoulders.png",
            Slot.CHEST : "cloth_chest.png",
            Slot.HANDS : "cloth_hands.png",
            Slot.LEGS : "cloth_legs.png",
            Slot.FEET : "cloth_feet.png"
        }
        self.leather_material_image = {
            Slot.HEAD : "leather_head.png",
            Slot.SHOULDERS : "leather_shoulders.png",
            Slot.CHEST : "leather_chest.png",#
            Slot.HANDS : "leather_hands.png",
            Slot.LEGS : "leather_legs.png",
            Slot.FEET : "leather_feet.png"
        }
        self.metal_material_image = {
            Slot.HEAD : "metal_head.png",
            Slot.SHOULDERS : "metal_shoulders.png",
            Slot.CHEST : "metal_chest.png",
            Slot.HANDS : "metal_hands.png",
            Slot.LEGS : "metal_legs.png",
            Slot.FEET : "metal_feet.png"
        }                
        self.rarity_border = {
            Rarity.COMMON : "common_border.png",
            Rarity.UNCOMMON : "uncommon_border.png",
            Rarity.RARE : "rare_border.png",
            Rarity.EPIC : "epic_border.png"            
        }
        self.leather_name = {
            Slot.HEAD : "Cap",
            Slot.SHOULDERS : "Mantle",
            Slot.CHEST : "Tunic",
            Slot.HANDS : "Grips",
            Slot.LEGS : "Leggings",
            Slot.FEET : "Boots"
        }
        self.cloth_name = {
            Slot.HEAD : "Hat",
            Slot.SHOULDERS : "Drape",
            Slot.CHEST : "Shirt",
            Slot.HANDS : "Gloves",
            Slot.LEGS : "Robe",
            Slot.FEET : "Slippers"
        }
        self.metal_name = {
            Slot.HEAD : "Helmet",
            Slot.SHOULDERS : "Pauldron",
            Slot.CHEST : "Platebody",
            Slot.HANDS : "Gauntlets",
            Slot.LEGS : "Platelegs",
            Slot.FEET : "Heavy Boots"
        }     
        self.stat_quality = {
            Rarity.COMMON : 1,
            Rarity.UNCOMMON : 2,
            Rarity.RARE : 3,
            Rarity.EPIC : 4
        }
        self.material_switch = {
            Material.CLOTH : self.cloth_name,
            Material.LEATHER : self.leather_name,
            Material.METAL : self.metal_name
        }
        self.material_image_switch = {
            Material.CLOTH : self.cloth_material_image,
            Material.LEATHER : self.leather_material_image,
            Material.METAL : self.metal_material_image
        }
        self.slot = {
            0 : Slot.HEAD,
            1 : Slot.SHOULDERS,
            2 : Slot.CHEST,
            3 : Slot.HANDS,
            4 : Slot.LEGS,
            5 : Slot.FEET
        }
        self.material = {
            0 : Material.CLOTH,
            1 : Material.LEATHER,
            2 : Material.METAL
        }
        self.rarity = {
            0 : Rarity.COMMON,
            1 : Rarity.UNCOMMON,
            2 : Rarity.RARE,
            3 : Rarity.EPIC
        }
        self.stats = {
           0 : Stat.STRENGTH,
           1 : Stat.DEXTERITY,
           2 : Stat.CONSTITUTION,
           3 : Stat.INTELLIGENCE,
           4 : Stat.WISDOM,
           5 : Stat.FLAT_DR,
           6 : Stat.PERCENT_DR,
           7 : Stat.DEFENCE
        }


    def form_new_equipment(self):
        self.equip_slot = self.slot[random.randint(0, 5)]
        self.equip_material = self.material[random.randint(0, 2)]
        self.equip_rarity = self.rarity[random.randint(0, 3)]
        self.generate_stats()
        self.set_name()
        self.set_image()
        print("New equipment formed!")
        
    def generate_stats(self):
        stat_mag = []
        random_stat = []
        check_stat = Stat
        while len(random_stat) < self.stat_quality[self.equip_rarity]:
            check_stat = self.stats[random.randint(0, 7)]
            if random_stat.count(check_stat) == 0:
                random_stat.append(check_stat)
        for stat in random_stat:
            stat_mag = random.randint(self.stat_range[self.equip_rarity][0], self.stat_range[self.equip_rarity][1])
            # *self.stat_range[self.equip_rarity]
            self.stat_changes[stat] = stat_mag

    def set_name(self, name = ""):
        if name:
            self.name = name
        else:
            self.name = self.material_name[self.equip_material] + " " + self.material_switch[self.equip_material][self.equip_slot]

    def set_image(self, image = ""):
        if image:
            self.image = image
        else:
            self.image = self.material_image_switch[self.equip_material][self.equip_slot]
        