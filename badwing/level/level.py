from pytmx import TiledMap

from crunge.engine.d2.physics import PhysicsEngine

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
#from badwing.model import Model
from badwing.dialogs.pause import PauseDialog
from badwing.dialogs.beatlevel import BeatLevelDialog

class Level(Scene):
    def __init__(self, name):
        super().__init__(name)
        badwing.app.scene = self
        self.physics_engine: PhysicsEngine = None
        self.pc_stack = []
        self.tilewidth = 0
        self.tileheight = 0

        #self.song = arcade.load_sound(asset('music/funkyrobot.mp3'))

    @property
    def pc(self):
        return self.pc_stack[-1]

    '''
    @property
    def pc_sprite(self):
        return self.pc.vu
        #return self.pc
    '''

    def push_pc(self, pc):
        self.pc_stack.append(pc)
        badwing.app.pc = pc
        #self.pc_sprite = pc.sprite
        self.push_controller(pc.control())

    def pop_pc(self):
        pc = self.pc_stack.pop()
        badwing.app.pc = pc
        #self.pc_sprite = pc.sprite
        self.pop_controller()
        return pc

    def beat_level(self):
        next_level = self.get_next_level()
        self.open_dialog(BeatLevelDialog(next_level))

    def _create(self):
        super()._create()

        #map_name = asset(f"{self.name}.json")
        tmx_path = asset(f"{self.name}.tmx")
        self.map = map = self.map = TiledMap(tmx_path)
        #print('level setup')

        self.tilewidth = map.tilewidth
        self.tileheight = map.tileheight
        #self.width = map.width * self.tilewidth
        #self.height = map.height * self.tileheight
        self.top = self.height
        self.right = self.width
        #print('width:  ', self.width)
        #print('height:  ', self.height)

    def update(self, delta_time):

        super().update(delta_time)

        if not self.paused:
            #seems to floaty to me:
            #self.physics_engine.update(delta_time)
            self.physics_engine.update(1/60)
            self.check_collisions()

        if badwing.app.player.level_beat:
            self.beat_level()
            badwing.app.player.level_beat = False
            #return

    def check_collisions(self):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.open_dialog(PauseDialog())

        self.controller.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.controller.on_key_release(key, modifiers)
