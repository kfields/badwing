from loguru import logger

import glm

from crunge.engine.d2.entity import StaticEntity2D

from badwing.constants import *
from badwing.scene_layer import SceneLayer


class Tile(StaticEntity2D):
    def __init__(self, position, vu, sprite):
        super().__init__(position, vu=vu, model=sprite)


class TileLayer(SceneLayer):
    def __init__(self, name, factory=None):
        super().__init__(name, factory)
