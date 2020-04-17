import math
import random
import arcade
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull
import badwing.app
from badwing.constants import *
from badwing.model import Model
from badwing.sticker import StickerLayer

class Coin(Model):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, sprite):
        kind = sprite.properties['type']
        model = kinds[kind].create(sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model


class Gem(Coin):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

    @classmethod
    def create(self, sprite):
        return Gem(sprite, position=(0,0))


class CoinLayer(StickerLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            model = Coin.create(sprite)
            self.add_model(model)

kinds = {
    'coin': Gem
}