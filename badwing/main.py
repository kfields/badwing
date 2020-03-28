import sys
import os

import arcade
import pymunk

from badwing import __version__
import badwing.app
import badwing.assets
from badwing.assets import asset
from badwing.constants import *
from badwing.player import Player
#from badwing.levels.level1 import Level
from badwing.levels.start import StartScreen

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        badwing.app.game = self

        self.theme = None

        self.player = Player()

    def show_scene(self, scene):
        self.scene = scene
        self.show_view(scene)

    def setup(self):
        self.set_theme()
        self.scene.setup()
        self.scene.post_setup()

    def set_dialogue_box_texture(self):
        dialogue_box = asset("gui_themes/Fantasy/DialogueBox/DialogueBox.png")
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_button_texture(self):
        normal = asset("gui_themes/Fantasy/Buttons/Normal.png")
        hover = asset("gui_themes/Fantasy/Buttons/Hover.png")
        clicked = asset("gui_themes/Fantasy/Buttons/Clicked.png")
        locked = asset("gui_themes/Fantasy/Buttons/Locked.png")
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def set_theme(self):
        self.theme = arcade.gui.Theme()
        self.set_dialogue_box_texture()
        self.set_button_texture()
        self.theme.set_font(24, arcade.color.BLACK, font_name='Verdana')

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.scene.draw()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if badwing.app.avatar:
            badwing.app.avatar.update(delta_time)
        self.player.update(delta_time)
        self.scene.update(delta_time)

def main(production=False):
    pip_assets_dir = os.path.join(sys.prefix, 'share/badwing/assets')
    is_pip_install = os.path.isdir(pip_assets_dir)
    if is_pip_install:
        badwing.assets.assets_dir = pip_assets_dir
    else:
        badwing.assets.assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../assets')
    
    if not production:
        if is_pip_install:
            raise Exception('You need to run this in the project root directory!')
    else:
        pass
    
    """ Main method """
    window = MyGame()
    scene = StartScreen()
    window.show_scene(scene)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
