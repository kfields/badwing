import math
import random
import arcade
import pymunk

import badwing.app
from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce
from badwing.model import Model, Group, ModelFactory
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
    def __init__(self, position, sprite):
        super().__init__(position, sprite)
        self.collected = False

class Flag(Model):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)
        self.collected = False

    @classmethod
    def create(self, position, sprite):
        kind = sprite.properties['type']
        model = kinds[kind].create(position, sprite)
        return model

    def collect(self):
        if self.collected:
            return True
        self.collected = collected = True
        #TODO: not working as planned
        old_sprite = self.sprite
        self.sprite = sprite = arcade.Sprite()
        sprite.texture = old_sprite.texture
        old_sprite.remove_from_sprite_lists()
        return collected


class FlagGreen(Flag):
    @classmethod
    def create(self, position, sprite):
        return FlagGreen(position, sprite)

class FlagYellow(Flag):
    @classmethod
    def create(self, position, sprite):
        return FlagYellow(position, sprite)

class FlagRed(Flag):
    @classmethod
    def create(self, position, sprite):
        return FlagRed(position, sprite)

kinds = {
    'Pole': Pole,
    'FlagGreen': FlagGreen,
    'FlagYellow': FlagYellow,
    'FlagRed': FlagRed,
}

class FlagFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        for sprite in self.layer.sprites:
            kind = sprite.properties['type']
            if kind == 'Pole':
                model = Pole(sprite.position, sprite)
            else:
                model = Flag.create(sprite.position, sprite)
            self.layer.add_model(model)
