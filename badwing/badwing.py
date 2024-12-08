import sys
import os

import inspect
from importlib import import_module

from loguru import logger
import glm

from crunge.engine import App, Renderer
from crunge.engine.channel import Channel
from crunge.engine.scheduler import Scheduler
from crunge.engine.resource.resource_manager import ResourceManager

from badwing import __version__
import badwing.globe
from badwing.assets import asset
from badwing.constants import *
from badwing.player import Player

from .scene import Scene
from .scene_view import SceneView


class BadWing(App):
    def __init__(self, debug=False):
        super().__init__(glm.ivec2(SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_TITLE)
        badwing.globe.game = self
        self.debug = debug
        self.scene = None
        self.player = Player()

    def install(self, name):
        logger.debug(f"Installing: {name}")
        import importlib.util
        spec = importlib.util.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    """
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
            self.scene = scene = scene_class.produce().config(size=self.size).create()
            self.view = SceneView(scene).config(window=self)
        Scheduler().schedule_once(callback, delay)
    """

    def update(self, delta_time: float):
        self.player.update(delta_time)
        super().update(delta_time)


def main(debug=False, levelname="start"):
    """Main method"""

    pip_assets_dir = os.path.join(sys.prefix, "share/badwing/assets")
    is_pip_install = os.path.isdir(pip_assets_dir)
    if is_pip_install:
        badwing.assets.assets_dir = pip_assets_dir
    else:
        badwing.assets.assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../assets")
        )

    ResourceManager().add_path_variable("resources", badwing.assets.assets_dir)

    game = BadWing(debug=debug)
    #game.use_channel('start')
    game.install('badwing.channels.start')
    game.install('badwing.channels.level1')
    #game.use_channel('level1')
    # game.show_scene(game.get_scene(levelname))
    game.show_channel(levelname)
    game.create().run()


if __name__ == "__main__":
    main()
