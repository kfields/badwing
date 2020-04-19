import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
import badwing.assets as assets
from badwing.model import StaticModel, ModelFactory
from badwing.layer import Layer

class Tile(StaticModel):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    def update(self, dt):
        super().update(dt)
        if not DEBUG_COLLISION:
            return
        #line_strip = arcade.create_line_strip(sprite.points, (255,255,255), 1)
        line_strip = arcade.create_lines(self.sprite.points, (0,0,0), 1)
        badwing.app.debug_layer.add(line_strip)


class TileLayer(Layer):
    def __init__(self, level, name, factory=None):
        super().__init__(level, name, factory)
        self.sprites = arcade.tilemap.process_layer(level.map, name, TILE_SCALING)


class TileFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        for sprite in self.layer.sprites:
            self.layer.add_model(Tile(sprite.position, sprite))
