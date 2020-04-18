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

from badwing.butterfly.brain import ButterflyBrain

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

RANGE = 512 # How far they can travel
HALF_RANGE = RANGE/2

class ButterflySprite(arcade.Sprite):
    def __init__(self, index, position):
        super().__init__(center_x=position[0], center_y=position[1])

        # Animation timing
        self.time = 1
        self.update_time = 0
        self.rate = 1/60
        self.angle = -45
        self.character_face_direction = RIGHT_FACING
        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # --- Load Textures ---
        texture_coords = []
        for i in range(FRAMES):
            texture_coords.append( (i*SPRITE_WIDTH*2, index*SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT) )
            texture_coords.append( (i*SPRITE_WIDTH*2+SPRITE_WIDTH, index*SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT) )

        self.walk_textures = arcade.load_textures(asset('sprites/butterflies.png'), texture_coords)
        self.idle_texture_pair = [self.walk_textures[0], self.walk_textures[1]]
        self.texture = self.idle_texture_pair[self.character_face_direction]

    @debounce(.1)
    def face_left(self):
        self.character_face_direction = LEFT_FACING
        self.angle = 45

    @debounce(.1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING
        self.angle = -45

    def update_animation(self, delta_time: float = 1/60):
        self.time += delta_time

        if self.update_time > self.time:
            return
        self.update_time = self.time + self.rate

        r = random.randint(0, 2)
        if r == 0:
            self.rate += RATE_DELTA
        elif r == 2: 
            self.rate -= RATE_DELTA
        if self.rate < RATE_MIN:
            self.rate = RATE_DELTA
        elif self.rate > RATE_MAX:
            self.rate = RATE_DELTA

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.face_left()
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.face_right()
        
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        # Walking animation
        self.cur_texture += 1

        if self.cur_texture > FRAMES-1:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture * 2 + self.character_face_direction]

class Butterfly(Model):
    def __init__(self, position=(0,0), sprite=None, border=(0,0,640,480)):
        super().__init__(position, sprite, brain=ButterflyBrain(self))
        self.border = border

    @classmethod
    def create(self, kind, position=(0,0), border=(0,0,640,480)):
        model = kinds[kind].create(position, border)
        return model

    @classmethod
    def create_from(self, sprite):
        kind = sprite.properties['type']
        pos = sprite.position
        border = (pos[0]-HALF_RANGE, pos[1]-HALF_RANGE, pos[0]+HALF_RANGE, pos[1]+HALF_RANGE)
        model = kinds[kind].create(pos, border)
        return model

class ButterflyAqua(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(8, position)
        return ButterflyAqua(position, sprite, border)

class ButterflyBlue(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(0, position)
        return ButterflyBlue(position, sprite, border)

class ButterflyBrown(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(4, position)
        return ButterflyBrown(position, sprite, border)

class ButterflyCyan(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(5, position)
        return ButterflyCyan(position, sprite, border)

class ButterflyGreen(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(1, position)
        return ButterflyGreen(position, sprite, border)

class ButterflyIridescent(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(6, position)
        return ButterflyIridescent(position, sprite, border)

class ButterflyRed(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(7, position)
        return ButterflyRed(position, sprite, border)

class ButterflyTan(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(3, position)
        return ButterflyTan(position, sprite, border)

class ButterflyTeal(Butterfly):
    @classmethod
    def create(self, position, border=(0,0,640,480)):
        sprite = ButterflySprite(2, position)
        return ButterflyTeal(position, sprite, border)


kinds = {
    'ButterflyBlue': ButterflyBlue,
    'ButterflyAqua': ButterflyAqua,
    'ButterflyBrown': ButterflyBrown,
    'ButterflyCyan': ButterflyCyan,
    'ButterflyGreen': ButterflyGreen,
    'ButterflyIridescent': ButterflyIridescent,
    'ButterflyRed': ButterflyRed,
    'ButterflyTan': ButterflyTan,
    'ButterflyTeal': ButterflyTeal
}

kinds_list = list(kinds)

class Butterflies(Group):
    def __init__(self, border=(0,0,640,480)):
        super().__init__()

    @classmethod
    def create_random(self, count, border=(0,0,640,480)):
        group = Butterflies()
        for i in range(count):
            center_x = random.randint(0, border[2])
            center_y = random.randint(0, border[3])
            position = (center_x, center_y)
            ndx = random.randint(0, 8)
            kind = kinds_list[ndx]
            butterfly = Butterfly.create(kind, position, border)
            group.add_model(butterfly)
        return group

class ButterflyFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        orig_sprites = self.layer.sprites
        self.layer.sprites = arcade.SpriteList()

        for sprite in orig_sprites:
            #print(sprite)
            kind = sprite.properties.get('type')
            if not kind:
                continue
            position = sprite.position
            model = Butterfly.create_from(sprite)
            #print(model)
            self.layer.add_model(model)
