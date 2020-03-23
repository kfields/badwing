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
        self.debug_list = arcade.ShapeElementList()
    
    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def setup(self):
        map_name = f"assets/map/{self.name}.tmx"
        self.map = arcade.tilemap.read_tmx(map_name)
        for layer in self.layers:
            layer.setup()

    def update(self, dt):
        for layer in self.layers:
            layer.update(dt)
        self.space.step(1 / 60.0)

    def draw(self):
        for layer in self.layers:
            layer.draw()
        self.debug_list.draw()
        self.debug_list = arcade.ShapeElementList()

    def load(filename):
        with open(filename) as f:
            map = json.load(f)
        self.load_layers(map.layers)

    def load_layers(map_layers):
        for map_layer in map_layers:
            layer = Layer(self)
            layer.load(map_layer)
            self.layers[map_layer.name] = layer
