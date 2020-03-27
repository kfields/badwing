import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.model import Model

class Level:
    def __init__(self, name):
        badwing.app.level = self
        self.name = name
        self.layers = []
        self.width = 0
        self.height = 0
        self.tilewidth = 0
        self.tileheight = 0

        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
    
    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def setup(self):
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

    def post_setup(self):
        for layer in self.layers:
            layer.setup()

    def update(self, dt):
        for layer in self.layers:
            layer.update(dt)
        self.space.step(1 / 60.0)

    def draw(self):
        for layer in self.layers:
            layer.draw()