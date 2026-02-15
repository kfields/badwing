from loguru import logger

import glm

from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.scene.layer import GraphLayer2D

from badwing.constants import *


class Tile(StaticEntity2D):
    def __init__(self, position, vu, sprite):
        super().__init__(position, vu=vu, model=sprite)


class TileLayer(GraphLayer2D):
    def __init__(self, name):
        super().__init__(name)
