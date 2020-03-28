import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.scene import Scene
from badwing.model import Model

class Level(Scene):
    def __init__(self, name):
        super().__init__(name)
        badwing.app.level = self

        self.tilewidth = 0
        self.tileheight = 0
    
    def setup(self):
        super().setup()
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
        self.space.step(1 / 60.0)
