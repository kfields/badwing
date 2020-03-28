import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.model import Model

class Scene(arcade.application.View):
    def __init__(self, name):
        super().__init__()
        badwing.app.scene = self
        self.name = name
        self.layers = []
        self.width = 0
        self.height = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
    
    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def setup(self):
        pass

    def post_setup(self):
        for layer in self.layers:
            layer.setup()

    def update(self, delta_time):
        super().update(delta_time)
        for layer in self.layers:
            layer.update(delta_time)

    def draw(self):
        self.on_draw()

    def on_draw(self):
        for layer in self.layers:
            layer.draw()
        super().on_draw()
