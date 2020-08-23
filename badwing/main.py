import sys
import os

import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

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
    def __init__(self, debug=False):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        badwing.app.game = self
        self.debug = debug
        self.scene = None
        self.theme = None
        self.player = Player()

    @property
    def controller(self):
        return badwing.app.controller

    def get_scene(self, scenename=None):
        if scenename:
            #path = os.path.abspath(os.path.dirname(__file__))
            #path = os.path.join(path, f"../scenes/{scenename}")
            #imported_module = import_module('.' + scenename, package=__name__)
            imported_module = import_module('.' + scenename, package='badwing.scenes')
            for i in dir(imported_module):
                attribute = getattr(imported_module, i)
                if inspect.isclass(attribute) and issubclass(attribute, Scene):
                    return attribute

        if self.debug:
            from badwing.scenes.level1 import Level1
            return Level1
        else:
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
        pass
        '''
        self.theme = arcade.gui.Theme()
        self.set_dialogue_box_texture()
        self.set_button_texture()
        self.theme.set_font(24, arcade.color.BLACK, font_name='Verdana')
        '''

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.scene.draw()

    def update(self, delta_time):
        super().update(delta_time)
        self.player.update(delta_time)

def main(debug=False, levelname=None):
    #print(levelname)
    pip_assets_dir = os.path.join(sys.prefix, 'share/badwing/assets')
    is_pip_install = os.path.isdir(pip_assets_dir)
    if is_pip_install:
        badwing.assets.assets_dir = pip_assets_dir
    else:
        badwing.assets.assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../assets')
        
    """ Main method """
    game = MyGame(debug=debug)
    game.show_scene(game.get_scene(levelname))
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
