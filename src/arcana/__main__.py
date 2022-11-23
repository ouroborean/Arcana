import sdl2.ext
from shikkoku.app import App

from arcana.game_scene import GameScene
from arcana.cc_scene import CCScene
from arcana.menu_scene import MenuScene

FONTNAME = "Basic-Regular.ttf"

def main():
    """Main game entry point."""

    with App("Arcana", (1200, 800)) as app:
        app.assign_resource_path("arcana.resources")
        app.assign_font(app.init_font(16, FONTNAME))
        app.add_scene(GameScene(app, "game"))
        app.add_scene(CCScene(app, "cc"))
        app.add_scene(MenuScene(app, "menu"))
        app.start_game_loop(app.scenes["menu"])
    
main()