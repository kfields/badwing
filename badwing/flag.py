import math
import random
import arcade
import pymunk

import badwing.app
from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce
from badwing.model import Model, Group
from badwing.tile import TileLayer

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32
CHARACTER_SCALING = 1

MOVEMENT_SPEED = 5
FRAMES = 10
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

RATE_DELTA = 1/60
RATE_MIN = 0
RATE_MAX = .1

class Pole(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.collected = False

class Flag(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.collected = False

    @classmethod
    def create(self, sprite):
        kind = sprite.properties['kind']
        model = kinds[kind].create(sprite)
        return model

    def collect(self):
        if self.collected:
            return True
        self.collected = collected = True
        #TODO: not working as planned
        old_sprite = self.sprite
        self.sprite = sprite = arcade.Sprite()
        sprite.texture = old_sprite.texture
        old_sprite.kill()
        return collected


class FlagGreen(Flag):
    @classmethod
    def create(self, sprite):
        return FlagGreen(sprite)

class FlagYellow(Flag):
    @classmethod
    def create(self, sprite):
        return FlagYellow(sprite)

class FlagRed(Flag):
    @classmethod
    def create(self, sprite):
        return FlagRed(sprite)

kinds = {
    'Pole': Pole,
    'FlagGreen': FlagGreen,
    'FlagYellow': FlagYellow,
    'FlagRed': FlagRed,
}

class FlagTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            kind = sprite.properties['kind']
            if kind == 'Pole':
                model = Pole(sprite)
            else:
                model = Flag.create(sprite)
            #print('flag sprite')
            #print(vars(sprite))
            #print(sprite.properties)
            #print('flag')
            #print(vars(model))
            self.add_model(model)

