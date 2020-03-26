import json
import arcade
import pymunk

from badwing.constants import *
import badwing.assets as assets
import badwing.app
from badwing.model import Model

class Level:
    def __init__(self, name):
        badwing.app.level = self
        self.name = name
        self.layers = []
    
    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def setup(self):
        map_name = f"assets/{self.name}.tmx"
        self.map = arcade.tilemap.read_tmx(map_name)

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