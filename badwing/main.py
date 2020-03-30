import sys
import os

import arcade
import pymunk
import pyglet

from badwing import __version__
import badwing.app
from badwing.assets import asset
from badwing.constants import *
from badwing.player import Player

from badwing.scene import Scene

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        badwing.app.game = self

        self.scene = None
        self.theme = None
        self.player = Player()

    def get_start_scene(self):
        from badwing.scenes.start import StartScene
        return StartScene

    def show_scene(self, scene_class, delay=0):

        if self.scene:
            self.scene.shutdown()

        def callback(delta_time):
            #print('show_scene')
            #TODO: Why is this not working?
            #if not isinstance(scene_class, badwing.scene.Scene):
            if not isinstance(scene_class, type):
                raise Exception(f'{scene_class} Must be a Scene class!')

            self.player.on_next_level()
            self.scene = scene = scene_class.create()
            self.show_view(scene)
        pyglet.clock.schedule_once(callback, delay)

    def setup(self):
        self.set_theme()

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

    def update(self, delta_time):
        super().update(delta_time)
        if badwing.app.avatar:
            badwing.app.avatar.update(delta_time)
        self.player.update(delta_time)

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
    game = MyGame()
    game.show_scene(game.get_start_scene())
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
