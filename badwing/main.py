import sys
import os

import inspect
from importlib import import_module

import glm

from crunge.engine import App, Renderer
from crunge.engine.scheduler import Scheduler
from crunge.engine.resource.resource_manager import ResourceManager

from badwing import __version__
import badwing.app
from badwing.assets import asset
from badwing.constants import *
from badwing.player import Player

from badwing.scene import Scene

class MyGame(App):
    def __init__(self, debug=False):
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        super().__init__(glm.ivec2(SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_TITLE)
        
        badwing.app.game = self
        self.debug = debug
        #self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.scene = None
        self.theme = None
        self.player = Player()

    @property
    def controller(self):
        return badwing.app.controller

    def get_scene(self, scenename=None):
        if scenename:
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
            if not isinstance(scene_class, type):
                raise Exception(f'{scene_class} Must be a Scene class!')

            self.player.on_next_level()
            self.scene = scene = scene_class.produce().config(window=self)
            self.view = scene
        Scheduler().schedule_once(callback, delay)

    '''
    def draw(self, renderer: Renderer):
        super().draw(renderer)
        #self.scene.draw(renderer)
        #badwing.app.physics_engine.space.debug_draw(self.draw_options)
    '''

    def update(self, delta_time):
        super().update(delta_time)
        self.player.update(delta_time)

def main(debug=False, levelname=None):
    """ Main method """

    pip_assets_dir = os.path.join(sys.prefix, 'share/badwing/assets')
    is_pip_install = os.path.isdir(pip_assets_dir)
    if is_pip_install:
        badwing.assets.assets_dir = pip_assets_dir
    else:
        badwing.assets.assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets'))
        
    ResourceManager().add_path_variable('resources', badwing.assets.assets_dir)
    
    game = MyGame(debug=debug)
    game.show_scene(game.get_scene(levelname))
    game.create().run()


if __name__ == "__main__":
    main()
