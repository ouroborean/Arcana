import sdl2.ext
from shikkoku.app import App

from arcana.game_scene import GameScene

FONTNAME = "Basic-Regular.ttf"

def main():
    """Main game entry point."""

    with App("Arcana", (1200, 800)) as app:
        app.assign_resource_path("arcana.resources")
        app.assign_font(app.init_font(16, FONTNAME))
        app.add_scene(GameScene(app, "game"))
        app.start_game_loop(app.scenes["game"])
    
main()