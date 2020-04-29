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

from badwing.characters.butterfly.brain import ButterflyBrain

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
        self.model.angle = 45

    @debounce(.1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING
        self.model.angle = -45

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
