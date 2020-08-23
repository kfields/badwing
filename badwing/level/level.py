import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
from badwing.model import Model
from badwing.dialogs.pause import PauseDialog
from badwing.dialogs.beatlevel import BeatLevelDialog

class Level(Scene):
    def __init__(self, name):
        super().__init__(name)
        badwing.app.scene = self
        self.physics_engine = None
        self.pc_stack = []
        self.tilewidth = 0
        self.tileheight = 0

        self.song = arcade.load_sound(asset('music/funkyrobot.ogg'))

    @property
    def pc(self):
        return self.pc_stack[-1]

    @property
    def pc_sprite(self):
        return self.pc.sprite

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

    def do_setup(self):
        super().do_setup()

        map_name = asset(f"{self.name}.tmx")
        self.map = tmx = arcade.tilemap.read_tmx(map_name)
        #print('level setup')

        self.tilewidth = tmx.tile_size.width
        self.tileheight = tmx.tile_size.height
        self.width = tmx.map_size.width * self.tilewidth
        self.height = tmx.map_size.height * self.tileheight
        self.top = self.height
        self.right = self.width
        #print('width:  ', self.width)
        #print('height:  ', self.height)

    def update(self, delta_time):

        super().update(delta_time)

        if not self.paused:
            #seems to floaty to me:
            #self.physics_engine.update(delta_time)
            self.physics_engine.update(1/40)
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
