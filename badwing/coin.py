import math
import random

import glm

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

import badwing.app
from badwing.constants import *
from badwing.model import Model
from badwing.model_factory import ModelFactory

class Coin(Model):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position, sprite):
        kind = sprite.properties['class']
        model = kinds[kind].produce(position, sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model


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
            model = Coin.produce(sprite.position, sprite)
            self.layer.add_model(model)

kinds = {
    'coin': Gem
}