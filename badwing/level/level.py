import glm

from crunge.engine.d2.physics import PhysicsEngine2D

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
from badwing.dialogs.pause import PauseDialog
from badwing.dialogs.beatlevel import BeatLevelDialog

from ..map.map_loader import MapLoader


class Level(Scene):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)
        badwing.globe.scene = self
        self.tilewidth = 0
        self.tileheight = 0

    def beat_level(self):
        next_level = self.get_next_level()
        self.open_dialog(BeatLevelDialog(next_level))

    def _create(self):
        super()._create()
        tmx_path = asset(f"{self.name}.tmx")
        map_loader = MapLoader(self)
        map_loader.load(tmx_path)

    def update(self, delta_time):

        super().update(delta_time)

        if not self.paused:
            #seems to floaty to me:
            #self.physics_engine.update(delta_time)
            self.physics_engine.update(1/60)
            self.check_collisions()

        if badwing.globe.player.level_beat:
            self.beat_level()
            badwing.globe.player.level_beat = False

    def check_collisions(self):
        pass

    '''
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.open_dialog(PauseDialog())

        self.controller.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.controller.on_key_release(key, modifiers)
    '''