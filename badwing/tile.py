from loguru import logger

import glm
import json
import pymunk

from crunge.engine.math import Rect2i
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.resource.texture import Texture
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder

import badwing.globe
from badwing.constants import *
import badwing.assets as assets
from badwing.model_factory import ModelFactory
from badwing.scene_layer import SceneLayer


class Tile(StaticEntity2D):
    def __init__(self, position, vu, sprite):
        super().__init__(position, vu=vu, model=sprite)


class TileLayer(SceneLayer):
    def __init__(self, level, name, factory=None):
        super().__init__(level, name, factory)
        # self.map_layer = level.map.get_layer_by_name(name)


class TileFactory(ModelFactory):
    def __init__(self, layer: SceneLayer):
        super().__init__(layer)

    def process_tile(self, position: glm.vec2, image, properties):
        logger.debug(f"process_tile: {position}, {image}, {properties}")
        name = self.map.filename

        path = image[0]
        atlas = ImageTextureLoader().load(path)
        # logger.debug(f"atlas: {atlas}")
        sprite_builder = CollidableSpriteBuilder()
        rect = image[1]
        if rect:
            tx, ty, tw, th = rect
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th)).set_name(name)
        else:
            sprite = sprite_builder.build(atlas).set_name(name)

        logger.debug(f"sprite: {sprite}")

        vu = SpriteVu(sprite).create()
        self.layer.attach(Tile(position, vu, sprite))
