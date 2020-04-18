import math
import random
import arcade
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull
import badwing.app
from badwing.constants import *
from badwing.model import Model, ModelFactory

class Coin(Model):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    @classmethod
    def create(self, position, sprite):
        kind = sprite.properties['type']
        model = kinds[kind].create(position, sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model


class Gem(Coin):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def create(self, position=(0,0), sprite=None):
        return Gem(position, sprite)


class CoinFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        for sprite in self.layer.sprites:
            model = Coin.create(sprite.position, sprite)
            self.layer.add_model(model)

kinds = {
    'coin': Gem
}