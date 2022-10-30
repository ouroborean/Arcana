from shikkoku.engine import Scene
from shikkoku.color import *
import sdl2.ext
import sdl2.ext
import sdl2.sdlttf
from arcana.tile import Tile
from PIL import Image
from arcana.equipment import Slot
from arcana.npc import NPC
import importlib.resources
from arcana.player import Player
from arcana.direction import direction_to_pos, Direction
from arcana.area import area_db
import enum
import functools

@enum.unique
class Menu(enum.IntEnum):
    NONE = 0
    INVENTORY = 1
    SKILLS = 2
    OPTIONS = 3
    EQUIP = 4

class equip_slot(enum.IntEnum):
    HEAD = 0
    SHOULDERS = 1
    CHEST = 2
    HANDS = 3
    LEGS = 4
    FEET = 5

def get_image_from_path(file_name: str) -> Image:
    with importlib.resources.path('arcana.resources', file_name) as path:
        return Image.open(path)


FONTNAME = "Basic-Regular.ttf"

class GameScene(Scene):
    
    def __add__(self, other):
        return (self.loc[0] + other[0], self.loc[1] + other[1])

    def __init__(self, app, name):
        super().__init__(app, name)
        self.enemy_count = 0
        self.to_equip = None
        self.old_tile = (0, 0) 
        self.previous_x = 38
        self.cursor_x = 38
        self.cursor_y = 38
        self.direction_x = 0
        self.x_distance = 0
        self.y_distance = 0
        self.loc = (0, 0)
        self.previous_xy = (0, 0)
        self.direction_xy = (0, 0)
        self.previous_y = 38
        self.direction_y = 0
        self.target_radius = 1
        self.b_pressed = False
        self.to_inventory = None
        self.enemy_spawn_clicked = False
        self.p_pressed = False
        self.item_count = 0
        self.seen_tiles = { Tile }
        self.the_wheel = {
            0 : (0, -1),
            1 : (-1, 0),
            2 : (0, 1),
            3 : (1, 0),
            4 : (0, -1)
        }
        self.targets = []
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event
            # sdl2.SDL_MOUSEMOTION: self.handle_mouse_movement
            
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_z: self.press_z,
            sdl2.SDLK_p: self.press_p,
            sdl2.SDLK_b: self.press_b,
            sdl2.SDLK_w: self.press_up,
            sdl2.SDLK_KP_PLUS: self.press_plus,
            sdl2.SDLK_KP_MINUS: self.press_minus,
            sdl2.SDLK_a: self.press_left,
            sdl2.SDLK_s: self.press_down,            
            sdl2.SDLK_d: self.press_right,                        
            sdl2.SDLK_RIGHT: self.press_right,
            sdl2.SDLK_LEFT: self.press_left,
            sdl2.SDLK_UP: self.press_up,
            sdl2.SDLK_DOWN: self.press_down,
            sdl2.SDLK_SPACE: self.press_space
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.menu_state = {
            Menu.INVENTORY : False,
            Menu.SKILLS : False,
            Menu.OPTIONS : False,
            Menu.EQUIP : False
        }

        self.render_open_menu = {
            Menu.NONE : self.do_nothing,
            Menu.INVENTORY : self.render_inventory_menu,
            Menu.SKILLS : self.render_skill_menu,
            Menu.OPTIONS : self.render_options_menu,
            Menu.EQUIP : self.render_equip_menu
        }
        self.equip_slot_location = {
            Slot.HEAD : (0, 0),
            Slot.SHOULDERS : (74, 0),
            Slot.CHEST : (148, 0),
            Slot.HANDS : (0, 74),
            Slot.LEGS : (0, 148),
            Slot.FEET : (74, 74)
        }
        self.menu_toggle_switch = {
            Menu.INVENTORY : self.toggle_inventory_menu,
            Menu.SKILLS : self.do_nothing,
            Menu.OPTIONS : self.do_nothing,
            Menu.EQUIP : self.toggle_equip_menu
        }
        
        self.grids = [self.make_sprite(self.app.load("grid.png")) for _ in range(14*9)]
        
        self.title_font = self.app.init_font(24, FONTNAME)
        self.button_font = self.app.init_font(10, FONTNAME)
        self.game_region = self.region.subregion(5, 5, 913, 588)
        self.button_region = self.region.subregion(1000, 500, 150, 150)
        self.mouse_cursor = self.make_button(self.app.load("rogueplayer.png", width=50, height=50))
        self.inventory_region = self.region.subregion(200, 200, 600, 300)
        self.hovered_tile = None
        self.tile_select = None
        self.dest = None
        self.path = list()
        
        self.equipment_panel = None
        self.equip_slot_panels = [self.make_button(self.app.load("grid.png")) for _ in range(len(self.equip_slot_location.values()))]
        for i, slot in enumerate(self.equip_slot_panels):
            slot.click += self.inventory_item
            slot.item = i
            
        
        self.inventory_panel = None
        self.inventory_slot_panels = [self.make_button(self.app.load("grid.png")) for _ in range(16)]
        for i, slot in enumerate(self.inventory_slot_panels):
            slot.click += self.equip_item
            slot.item = i
            
        self.background_panel = None
        
        self.background = None
        self.game_panel = None
        
        self.enemy_button_icon = None
        self.button_region_panel = None
        self.bag_button = None
        self.equipment_button = None
        self.enemy_spawn_button = None
        self.item_drop_button = None
        self.options_button = None
        self.skills_button = None
        self.get_created_character(Player())
        print(self.player)
        self.load_into_area(area_db["test"])
        
    def render_equip_menu(self, reset=False):
        if not self.equipment_panel:
            self.equipment_panel = self.make_panel(WHITE, self.inventory_region.size())
        
        if reset:
            self.inventory_region.clear()
            self.inventory_region.add_sprite(self.equipment_panel, 0, 0)
            for i, panel in enumerate(self.equip_slot_panels):
                self.inventory_region.add_sprite(panel, self.equip_slot_location[i][0], self.equip_slot_location[i][1])
            for slot, gear in self.player.equipped.items():
                if gear:
                    self.inventory_region.add_sprite(gear.sprite, self.equip_slot_location[slot][0], self.equip_slot_location[slot][1])

    def render_inventory_menu(self, reset=False):
        if not self.inventory_panel:
            self.inventory_panel = self.make_panel(WHITE, self.inventory_region.size())
        if reset:
            self.inventory_region.clear()
            self.inventory_region.add_sprite(self.inventory_panel, 0, 0)
            for i, slot in enumerate(self.inventory_slot_panels):
                row = i // 4
                column = i % 4
                self.inventory_region.add_sprite(slot, 5 + column * 65 + (9*column), 5 + row * 65 + (9*row))
                if i < len(self.player.inventory) and self.player.inventory[i]:
                    self.inventory_region.add_sprite(self.player.inventory[i].sprite, 5 + column * 65 + (9*column), 5 + row * 65 + (9*row))

    def equip_item(self, button, event):
        if self.player.inventory[button.item]:
            self.to_equip = self.player.inventory[button.item]
            print(f"Transferring {button.item} to equipment!")
            self.to_inventory = self.player.equipped[self.to_equip.equip_slot]
            self.player.equipped[self.to_equip.equip_slot] = self.to_equip
            print(f"Player equipped {self.player.equipped[self.to_equip.equip_slot].name}")
            print(f"Inventory: {self.player.inventory}")
            placeholder = self.player.inventory.index(self.to_equip)
            print(placeholder)
            self.player.inventory.insert(placeholder, self.to_inventory)
            print(f"Inventory: {self.player.inventory}")
            self.player.inventory.remove(self.player.inventory[placeholder + 1])
            self.render(self.render_inventory_menu, True)

    def inventory_item(self, button, event):
        print(button.item.name)
        print(button.item.stat_changes)

    def full_render(self, reset=False):
        if not self.background_panel:
            self.background_panel = self.make_panel(BLACK, (1200, 800))
        
        if reset:
            self.region.clear()
            self.region.add_sprite(self.background_panel, 0, 0)
        
        self.render_game_region(reset)
        self.render_button_region(reset)
        
    def render_game_region(self, reset=False):
        if not self.game_panel:
            self.game_panel = self.make_panel(SILVER, self.game_region.size())
        VIEWPORT_WIDTH_IN_TILES = 14
        VIEWPORT_HEIGHT_IN_TILES = 9
        if reset:
            self.game_region.clear()
            self.game_region.add_sprite(self.game_panel, 0, 0)
            
            all_tiles = VIEWPORT_WIDTH_IN_TILES * VIEWPORT_HEIGHT_IN_TILES
            
            X_OFFSET_TRIGGER = 6
            Y_OFFSET_TRIGGER = 4
            X_OFFSET_LIMIT = self.tile_map.width - VIEWPORT_WIDTH_IN_TILES
            Y_OFFSET_LIMIT = self.tile_map.height - VIEWPORT_HEIGHT_IN_TILES
            
            
            player_pos = self.tile_map.coord_to_num(self.player.loc)
            current_row = player_pos // self.tile_map.width
            row_offset = max(0, current_row - Y_OFFSET_TRIGGER)
            current_column = player_pos % self.tile_map.width
            column_offset = max(0, current_column - X_OFFSET_TRIGGER)
            if row_offset > Y_OFFSET_LIMIT:
                row_offset = Y_OFFSET_LIMIT
            if column_offset > X_OFFSET_LIMIT:
                column_offset = X_OFFSET_LIMIT
            for i in range(all_tiles):
                current_i = i
                row = (current_i // VIEWPORT_WIDTH_IN_TILES)
                column = (current_i % VIEWPORT_WIDTH_IN_TILES)
                x = 2 + column * 65
                y = 2 + row * 65
                self.game_region.add_sprite(self.grids[i], 1 + column * 65, 1 + row * 65)
                tile = self.tile_map.get_tile((column + column_offset, row + row_offset))
                sprite = tile.sprite
                
                self.game_region.add_sprite(sprite, 2 + column * 65, 2 + row * 65)
                if tile.scenery:
                    self.game_region.add_sprite(tile.scenery.sprite, x, y = 2 + row * 65)
                # if tile.actor and not tile.actor == self.player:
                #     self.game_region.add_sprite(tile.actor.sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1] * 65)
                if tile in self.path:
                    self.game_region.add_sprite(tile.hover_lens, x, y = 2 + row * 65)
                elif tile in self.seen_tiles:
                    self.game_region.add_sprite(tile.range_lens, x, y = 2 + row * 65)
                # if tile.item_drop:
                #     self.game_region.add_sprite(tile.item_drop.sprite, 2 + tile.loc[0] * 65, 2 + tile.loc[1]* 65)
            
            self.tile_map.get_tile(self.player.loc).actor = self.player
            
            self.game_region.add_sprite(self.player.sprite, 2 + (self.player.x - column_offset) * 65, 2 + (self.player.y - row_offset) * 65)

            self.render_open_menu[self.check_open_menu()](reset)

    def render_button_region(self, reset=False):
        self.button_region.clear()
        if not self.button_region_panel:
            self.button_region_panel = self.make_panel(SILVER, self.button_region.size())
        
        if not self.bag_button:
            self.bag_button = self.make_panel_button(BLACK, (60, 30))
            self.bag_button = self.render_bordered_text(self.button_font, "INVENTORY", BLACK, WHITE, self.bag_button, 4, 6, 1)
            self.bag_button.menu = Menu.INVENTORY
            self.bag_button.click += functools.partial(self.check_for_menus, Menu.INVENTORY)
        
        if not self.enemy_spawn_button:
            self.enemy_spawn_button = self.make_panel_button(BLACK, (60, 30))
            self.enemy_spawn_icon = self.make_sprite(self.app.load("rogueplayer.png"), 30, 30)
            self.enemy_spawn_button.click += self.enemy_spawn_button_click
            
        if not self.item_drop_button:
            self.item_drop_button = self.make_panel_button(BLACK, (60, 30))
        
        if not self.equipment_button:
            self.equipment_button = self.make_panel_button(BLACK, (60, 30))
            self.equipment_button = self.render_bordered_text(self.button_font, "EQUIPMENT", BLACK, WHITE, self.equipment_button, 4, 6, 1)
            self.equipment_button.menu = Menu.EQUIP
            self.equipment_button.click += functools.partial(self.check_for_menus, Menu.EQUIP)
            
        if not self.options_button:
            self.options_button = self.make_panel_button(BLACK, (60, 30))
            self.options_button = self.render_bordered_text(self.button_font, "OPTIONS", BLACK, WHITE, self.options_button, 12, 6, 1)
        
        if not self.skills_button:
            self.skills_button = self.make_panel_button(BLACK, (60, 30))
            self.skills_button = self.render_bordered_text(self.button_font, "SKILLS", BLACK, WHITE, self.skills_button, 16, 6, 1)
        
        if reset:
            self.button_region.clear()
            self.button_region.add_sprite(self.button_region_panel, 0, 0)
            self.button_region.add_sprite(self.bag_button, 10, 10)
            self.button_region.add_sprite(self.enemy_spawn_button, 80, 10)
            self.button_region.add_sprite(self.item_drop_button, 10, 50)
            self.button_region.add_sprite(self.equipment_button, 80, 50)
            self.button_region.add_sprite(self.options_button, 10, 90)
            self.button_region.add_sprite(self.skills_button, 80, 90) 
            self.button_region.add_sprite(self.enemy_spawn_icon, 100, 10)       

    def do_nothing(self, reset=False):
        pass

    def toggle_equip_menu(self):
        if self.menu_state[Menu.EQUIP] == True:
            self.menu_state[Menu.EQUIP] = False
            self.inventory_region.clear()
        else:
            self.menu_state[Menu.EQUIP] = True
        self.render(self.render_game_region, True)

    def check_for_menus(self, opening_menu : Menu, button, event):
        if self.menu_state[button.menu] == True:
            self.menu_toggle_switch[opening_menu]()
        else:
            for menu, state in self.menu_state.items():
                self.menu_state[menu] = False
            
            self.menu_toggle_switch[opening_menu]()

    def toggle_inventory_menu(self):
        if self.menu_state[Menu.INVENTORY] == True:
            self.menu_state[Menu.INVENTORY] = False
            self.inventory_region.clear()
        else:
            self.menu_state[Menu.INVENTORY] = True           
        self.render(self.render_game_region, True)

    def render_skill_menu(self, reset=False):
        print("Skill Menu Opened!")
        pass

    def render_options_menu(self, reset=False):
        print("Options Menu Opened!")
        pass

    def check_open_menu(self):
        for menu, state in self.menu_state.items():
            if state:
                return menu         
        return Menu.NONE

    def get_created_character(self, player):
        self.player = player
        self.manifest_player(self.player)
        self.player.set_game_scene(self)

    def enemy_spawn_button_click(self, button, event):
        self.enemy_spawn_clicked = True

    def check_actors(self):
        for target in self.targets:
            target.turn_counter += self.player.speed
            while target.turn_counter >= target.speed:
                target.npc_think(self.send_tile(target))
                target.turn_counter -= target.speed  

    def send_tile(self, target):
        target_loc = self.tile_map.get_tile((target.loc))
        return target_loc
           
    def change_area(self, portal):
        self.path.clear()
        self.load_into_area(area_db[portal.area_dest])
        for exit_portal in self.tile_map.portals:
            if exit_portal.portal_id == portal.portal_id:
                self.player.loc = exit_portal.loc
        self.spawn_player(self.player, self.player.loc)
        self.render(reset=True)

    def enemy_spawn(self, tile, npc):
        self.manifest_npc(npc)
        self.tile_map.get_tile(tile.loc).actor = npc
        self.targets.append(npc)
        npc.loc = tile.loc
        self.enemy_spawn_clicked = False
            
    def spawn_player(self, player, loc):
        self.manifest_player(player)
        self.player.loc = loc
        self.tile_map.get_tile(loc).actor = player

    def handle_npc_death(self, npc):
        tile = self.tile_map.get_tile(npc.loc)
        npc.item_drop.form_new_equipment()
        #TODO move this function to the NPC, to first pass their specific weights
        #TODO and call with weights from the specific area, through the game scene class
        self.manifest_item(npc.item_drop, npc.loc)
        tile.item_drop = npc.item_drop
        self.targets.remove(npc)
        tile.actor = None
        
        
    def manifest_item(self, item, loc):
        item.sprite = self.make_sprite(self.app.load(item.image), 64, 64)
        item.loc = loc

    def is_tile_seen(self, tile):
        for tile in self.seen_tiles:
            if self.tile_map.get_tile(self.loc) == tile:
                return True
        return False

    def move(self, direction):
        self.loc = self + direction
        self.seen_tiles.add(self.tile_map.get_tile(self.loc))        

    def spin_the_wheel(self, tile, radius):
        if tile:
            self.loc = (tile.loc)
            for spin in range(len(self.the_wheel)-1):
                for y in range(radius):
                    self.loc = tile.loc
                    for z in range(radius - y):
                        self.move(self.the_wheel[spin]) 
                    for a in range(y):
                        self.move(self.the_wheel[spin + 1])

    def press_minus(self, event):
        if self.b_pressed:
            if self.target_radius > 1:
                self.target_radius -= 1
                self.seen_tiles.clear()
                self.spin_the_wheel(self.tile_map.get_tile(self.player.loc), self.target_radius)
                self.render(self.render_game_region, True)

    def press_plus(self, event):
        if self.b_pressed:
            self.target_radius += 1
            self.seen_tiles.clear()
            self.spin_the_wheel(self.tile_map.get_tile(self.player.loc), self.target_radius)
            self.render(self.render_game_region, True)
            
        
    def press_b(self, event):
        print("Pressed B")
        self.b_pressed = not self.b_pressed
        if self.b_pressed:
            self.target_radius = 4
            self.spin_the_wheel(self.tile_map.get_tile(self.player.loc), self.target_radius)
        else:
            self.seen_tiles.clear()
        self.render(self.render_game_region,True)
                
#region Tile Selection Functions
    def select_tile(self, button):
        if self.hovered_tile != button:
            self.hovered_tile = button
            self.path.clear()
            self.path.append(button)
            self.render(reset=True)

    def move_over_tile_wrapper(self, tile):
        
        def move_over_tile(button, event):
            if not button.state == sdl2.ext.HOVERED:
                self.hovered_tile = tile
                self.get_path_to_mouse()
                self.render(reset=True)
                
        return move_over_tile


    def get_path_to_mouse(self):
        if self.hovered_tile:
            self.path = self.tile_map.get_shortest_path(self.tile_map.get_tile(self.player.loc), self.hovered_tile)[1:]
#endregion
    
#region Keypress Functions

    def press_right(self, event):
        twople = self.player + direction_to_pos[Direction.EAST]
        self.player.check_player_bump(self.tile_map.get_tile(twople))     
        self.check_actors()
        self.render(self.render_game_region, True)
    
    def press_left(self, event):
        twople = self.player + direction_to_pos[Direction.WEST]      
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors() 
        self.render(self.render_game_region, True)

    def press_up(self, event):
        twople = self.player + direction_to_pos[Direction.NORTH]
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors()
        self.render(self.render_game_region, True)       
    
    def press_down(self, event):
        twople = self.player + direction_to_pos[Direction.SOUTH]       
        self.player.check_player_bump(self.tile_map.get_tile(twople))
        self.check_actors()  
        self.render(self.render_game_region, True) 

    def press_p(self, event):
        print("P pressed!")
        self.p_pressed = not self.p_pressed
        if self.p_pressed:
            print("Path Mode turned ON, so now showing path to mouse!")
            self.get_path_to_mouse()
        else:
            if self.hovered_tile:
                print("Path Mode turned OFF, so now showing selected tile")
                self.path.clear()
                self.path.append(self.hovered_tile)
        self.render(self.render_game_region, True)

    def press_z(self, event):
        self.player.player_stand(self.tile_map.get_tile(self.player.loc))
        self.check_actors()  
        self.render(self.render_game_region, True)

    def press_space(self, event):
        if self.path:
            direction_tuple = (0, 0)
            for direction, tile in self.tile_map.get_tile(self.player.loc).neighbor.items():
                if self.path[0] == tile:
                    direction_tuple = direction_to_pos[direction]
            twople = self.player + direction_tuple
            self.player.check_player_bump(self.tile_map.get_tile(twople))
            self.check_actors()            
            self.render(reset=True)

#endregion

 #region Arrow Keys Release Functions  
    def release_right(self, event):
        pass
    
    def release_left(self, event):
        pass
    
    def release_up(self, event):
        pass
    
    def release_down(self, event):
        pass
#endregion    

    def load_into_area(self, area):
        self.area = area
        self.tile_map = self.area.gen_tilemap()
        self.manifest_tilemap(self.tile_map)
        
    def manifest_tilemap(self, tile_map):
        for tile in tile_map.tiles:
            tile.sprite = self.make_button(self.app.load(tile.image_path), 64, 64)
            tile.sprite.click += self.click_tile
            # tile.sprite.motion += self.move_over_tile_wrapper(tile)
            tile.sprite.tile = tile
            tile.hover_lens = self.make_panel(TRANSPARENT_PURPLE, (64, 64))
            tile.range_lens = self.make_panel(TRANSPARENT_BLUE, (64, 64))
            tile.hostile_lens = self.make_panel(TRANSPARENT_RED, (64, 64))
            self.manifest_scenery(tile)
        if tile_map.enemies:
            for enemy, landing in zip(tile_map.enemies, tile_map.enemy_landings):
                self.enemy_spawn(tile_map.get_tile(tile_map.num_to_coord(landing)), enemy)
                
    def manifest_scenery(self, tile):
        if tile.scenery:
            tile.scenery.sprite = self.make_sprite(self.app.load(tile.scenery.image_path), 64, 64)
    
    def manifest_player(self, player):
        player.sprite = self.make_sprite(self.app.load(player.image), 64, 64)
    
    def manifest_npc(self, npc):
        npc.sprite = self.make_sprite(self.app.load(npc.image), 64, 64)
    
    def click_tile(self, button, sender):
        if self.enemy_spawn_clicked:
            self.enemy_spawn(button.tile, NPC())
            self.render(self.render_game_region, True)
            
#region Event Handlers    
    def handle_event(self, event):
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)
    
    def handle_key_down_event(self, event):
        if event.key.keysym.sym in self.key_down_event_handlers:
            self.key_down_event_handlers[event.key.keysym.sym](event)
    
    def handle_key_up_event(self, event):
        if event.key.keysym.sym in self.key_up_event_handlers:
            self.key_up_event_handlers[event.key.keysym.sym](event)
#endregion
    
    def update_scene_state(self):
        pass