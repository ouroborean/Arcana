from shikkoku.engine import Scene
from shikkoku.app import App
from shikkoku.color import *
import sdl2.ext

from arcana.cc_scene import CCScene

FONTNAME = "Basic-Regular.ttf"

class MenuScene(Scene):
    
    def __init__(self, app, name):
        super().__init__(app, name)
        self.event_handlers = {
            sdl2.SDL_KEYDOWN: self.handle_key_down_event,
            sdl2.SDL_KEYUP: self.handle_key_up_event
        }
        
        self.key_down_event_handlers = {
            sdl2.SDLK_RIGHT: self.press_right,
            sdl2.SDLK_LEFT: self.press_left,
            sdl2.SDLK_UP: self.press_up,
            sdl2.SDLK_DOWN: self.press_down
        }
        
        self.key_up_event_handlers = {
            sdl2.SDLK_RIGHT: self.release_right,
            sdl2.SDLK_LEFT: self.release_left,
            sdl2.SDLK_UP: self.release_up,
            sdl2.SDLK_DOWN: self.release_down
        }
        self.background_region = self.region.subregion(0, 0, 1200, 800)
        self.button_region = self.region.subregion(500, 600, 200, 200)
        self.title_font = self.app.init_font(40, FONTNAME)
        self.title_region = self.region.subregion(200, 200, 800, 60)
        
        self.title_panel = None
        self.menu_panel = None
        self.new_game_button = None
        self.exit_game_button = None
        self.background_panel = None

        
    def full_render(self, reset=False):
        if reset:
            self.region.clear()
        self.render_background_region(reset)
        self.render_title_region(reset)
        self.render_button_region(reset)
    
    def render_background_region(self, reset=False):
        if not self.background_panel:
            background_panel = self.make_panel(BLACK, self.background_region.size())
        if reset:
            self.background_region.add_sprite(background_panel, 0, 0)
            
    def render_button_region(self, reset=False):
        
        if reset:
            self.button_region.clear()
        
        if not self.menu_panel:
            self.menu_panel = self.make_panel(PURPLE, self.button_region.size())
        if not self.new_game_button:
            self.new_game_button = self.make_panel_button(BLUE, (190, 90))
            self.new_game_button = self.border_sprite(self.new_game_button, DARK_BLUE, 2)
            self.new_game_button = self.render_bordered_text(self.title_font, "New Game", BLACK, WHITE, self.new_game_button, 8, 13, 1)
            self.new_game_button.click += self.new_game_click
        if not self.exit_game_button:
            self.exit_game_button = self.make_panel_button(BLUE, (190, 90))
            self.exit_game_button = self.border_sprite(self.exit_game_button, DARK_BLUE, 2)
            self.exit_game_button = self.render_bordered_text(self.title_font, "Exit Game", BLACK, WHITE, self.exit_game_button, 8, 13, 1)
            self.exit_game_button.click += self.exit_game_click
        if reset:
            self.button_region.add_sprite(self.menu_panel, 0, 0)
            self.button_region.add_sprite(self.new_game_button, 5, 5)
            self.button_region.add_sprite(self.exit_game_button, 5, 105)
            

        
    def render_title_region(self, reset=False):
        
        if reset:
            self.title_region.clear()
        
        if not self.title_panel:
            self.title_panel = self.make_panel(RED, self.title_region.size())
            self.title_panel = self.render_bordered_text(self.title_font, "Rogue Inheritance", BLACK, WHITE, self.title_panel, 20, 10, 1)
        if reset:
            self.title_region.add_sprite(self.title_panel, 0, 0)
            
        
    def new_game_click(self, button, sender):
        print("New Game Clicked")
        self.app.change_scene("cc")


    def exit_game_click(self, button, sender):
        exit()

    def press_right(self, event):
        pass
    
    def press_left(self, event):
        pass
    
    def press_up(self, event):
        pass
    
    def press_down(self, event):
        pass
        
    def release_right(self, event):
        pass
    
    def release_left(self, event):
        pass
    
    def release_up(self, event):
        pass
    
    def release_down(self, event):
        pass
    
    def handle_event(self, event):
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)
    
    def handle_key_down_event(self, event):
        if event.key.keysym.sym in self.key_down_event_handlers:
            self.key_down_event_handlers[event.key.keysym.sym](event)
    
    def handle_key_up_event(self, event):
        if event.key.keysym.sym in self.key_up_event_handlers:
            self.key_up_event_handlers[event.key.keysym.sym](event)

    
    def update_scene_state(self):
        pass
            