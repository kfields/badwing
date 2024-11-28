import math
import random

import glm

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from crunge.engine.d2.node_2d import Node2D

import badwing.globe
from badwing.constants import *
from badwing.model_factory import ModelFactory

class Coin(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position, sprite):
        kind = sprite.properties['class']
        node = kinds[kind].produce(position, sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return node


class Gem(Coin):
    def __init__(self, position=glm.vec2(), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position=glm.vec2(), sprite=None):
        return Gem(position, sprite)


class CoinFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def _create(self):
        for sprite in self.layer.sprites:
            node = Coin.produce(sprite.position, sprite)
            self.layer.add_node(node)

kinds = {
    'coin': Gem
}