import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
import badwing.assets as assets
from badwing.model import Model
from badwing.layer import Layer

class Tile(Model):
    def __init__(self, sprite):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        self.body = body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pymunk.Vec2d(sprite.center_x, sprite.center_y)

        self.shape = shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10

class TileLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.sprites = arcade.tilemap.process_layer(level.map, name, TILE_SCALING)

class PhysicsTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            self.add_model(Tile(sprite))
            #
            line_strip = arcade.create_line_strip(sprite.points, (255,255,255), 1)
            #line_strip = arcade.create_lines(sprite.points, (255,255,255), 1)
            badwing.app.level.debug_list.append(line_strip)
