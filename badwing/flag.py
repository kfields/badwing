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
    def __init__(self, sprite, border=(0,0,640,480)):
        super().__init__(sprite)
        self.border = border

    @classmethod
    def create(self, kind, position=(0,0), border=(0,0,640,480)):
        model = kinds[kind].create(position, border)
        return model

    @classmethod
    def create_from(self, sprite):
        kind = sprite.properties['kind']
        pos = sprite.position
        border = (pos[0]-HALF_RANGE, pos[1]-HALF_RANGE, pos[0]+HALF_RANGE, pos[1]+HALF_RANGE)
        model = kinds[kind].create(pos, border)
        return model

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

class FlagTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        #self.sprites = arcade.SpriteList()
        for orig_sprite in orig_sprites:
            print(vars(orig_sprite))
            print(orig_sprite.properties)
            #model = Flag.create_from(orig_sprite)
            #self.add_model(model)

