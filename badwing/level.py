import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
from badwing.model import Model
from badwing.dialogs.pause import PauseDialog

class Level(Scene):
    def __init__(self, name):
        super().__init__(name)
        badwing.app.level = self

        self.tilewidth = 0
        self.tileheight = 0

        self.pause_dialog = PauseDialog()
    
    def setup(self):
        super().setup()
        self.pause_dialog.setup()

        map_name = asset(f"{self.name}.tmx")
        self.map = tmx = arcade.tilemap.read_tmx(map_name)
        print('level setup')

        self.tilewidth = tmx.tile_size.width
        self.tileheight = tmx.tile_size.height
        self.width = tmx.map_size.width * self.tilewidth
        self.height = tmx.map_size.height * self.tileheight
        self.top = self.height
        self.right = self.width
        print('width:  ', self.width)
        print('height:  ', self.height)

    def update(self, delta_time):
        super().update(delta_time)
        if not self.paused:
            self.space.step(1 / 60.0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.open_dialog(self.pause_dialog)
        badwing.app.avatar.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        badwing.app.avatar.on_key_release(key, modifiers)
