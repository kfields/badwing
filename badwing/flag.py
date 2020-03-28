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

class Flag(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.touched = False

    @classmethod
    def create(self, sprite):
        kind = sprite.properties['kind']
        model = kinds[kind].create(sprite)
        return model

    # Has been touched by player
    def touch(self):
        if self.touched:
            return False
        self.touched = touched = True
        #TODO: not working as planned
        old_sprite = self.sprite
        self.sprite = sprite = arcade.Sprite()
        sprite.texture = old_sprite.texture
        old_sprite.kill()
        return touched

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
    'FlagGreen': FlagGreen,
    'FlagYellow': FlagYellow,
    'FlagRed': FlagRed,
}

class FlagTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            #print('flag sprite')
            #print(vars(sprite))
            #print(sprite.properties)
            model = Flag.create(sprite)
            #print('flag')
            #print(vars(model))
            self.add_model(model)

