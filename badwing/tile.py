from loguru import logger

import glm
import json
import pymunk

from crunge.engine.math import Rect2i
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.resource.texture import Texture
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

import badwing.app
from badwing.constants import *
import badwing.assets as assets
from badwing.model import StaticModel
from badwing.model_factory import ModelFactory
from badwing.layer import Layer


class Tile(StaticModel):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    """
    def update(self, dt):
        super().update(dt)
        if not DEBUG_COLLISION:
            return
        #line_strip = arcade.create_line_strip(sprite.points, (255,255,255), 1)
        line_strip = arcade.create_lines(self.sprite.points, (0,0,0), 1)
        badwing.app.debug_layer.add(line_strip)
    """


class TileLayer(Layer):
    def __init__(self, level, name, factory=None):
        super().__init__(level, name, factory)
        #self.map_layer = level.map.get_layer_by_name(name)


class TileFactory(ModelFactory):
    def __init__(self, layer: Layer):
        super().__init__(layer)

    def process_tile(self, position: glm.vec2, image, properties):
        logger.debug(f"process_tile: {position}, {image}, {properties}")
        name = self.map.filename

        path = image[0]
        atlas = ImageTextureLoader().load(path)
        #logger.debug(f"atlas: {atlas}")

        rect = image[1]
        if rect:
            tx, ty, tw, th = rect
            sprite = Sprite(
                atlas,
                Rect2i(tx, ty, tw, th),
            ).set_name(name)
            #logger.debug(f"texture: {texture}")
        else:
            sprite = Sprite(atlas).set_name(name)

        sprite = SpriteVu(sprite).create()
        self.layer.add_model(Tile(position, sprite))
