from pytmx import TiledMap

from crunge.engine.d2.physics import PhysicsEngine

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
from badwing.dialogs.pause import PauseDialog
from badwing.dialogs.beatlevel import BeatLevelDialog

class Level(Scene):
    def __init__(self, name):
        super().__init__(name)
        badwing.globe.scene = self
        self.physics_engine: PhysicsEngine = None
        self.avatar_stack = []
        self.tilewidth = 0
        self.tileheight = 0

    @property
    def pc(self):
        return self.avatar_stack[-1]

    def push_avatar(self, avatar):
        self.avatar_stack.append(avatar)
        badwing.globe.avatar = avatar
        self.push_controller(avatar.control())

    def pop_avatar(self):
        avatar = self.avatar_stack.pop()
        badwing.globe.avatar = avatar
        self.pop_controller()
        return avatar

    def beat_level(self):
        next_level = self.get_next_level()
        self.open_dialog(BeatLevelDialog(next_level))

    def _create(self):
        super()._create()
        tmx_path = asset(f"{self.name}.tmx")
        self.map = map = self.map = TiledMap(tmx_path)

        self.tilewidth = map.tilewidth
        self.tileheight = map.tileheight

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
            #return

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