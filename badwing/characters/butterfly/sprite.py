import math
import random

from loguru import logger

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite_atlas_loader import SpriteAtlasLoader

from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce
from badwing.model import Model, Group
from badwing.model_factory import ModelFactory
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

class ButterflySprite(SpriteVu):
    def __init__(self, index):
        super().__init__()

        # Animation timing
        self.time = 1
        self.update_time = 0
        self.rate = 1/60
        self.angle = -45
        self.character_face_direction = RIGHT_FACING
        # Used for flipping between image sequences
        self.cur_texture = 0

        #self.scale = CHARACTER_SCALING

        # --- Load Textures ---
        sprite_rects = []
        for i in range(FRAMES):
            sprite_rects.append( Rect2i(i*SPRITE_WIDTH*2, index*SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT) )
            sprite_rects.append( Rect2i(i*SPRITE_WIDTH*2+SPRITE_WIDTH, index*SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT) )

        #self.walk_textures = TextureAtlasLoader().load(asset('sprites/butterflies.png'), texture_rects)
        self.walk_textures = SpriteAtlasLoader().load(asset('sprites/butterflies.png'), sprite_rects, name=f'butterflies{index}')
        self.idle_texture_pair = [self.walk_textures[0], self.walk_textures[1]]
        #self.texture = self.idle_texture_pair[self.character_face_direction]
        self.sprite = self.idle_texture_pair[self.character_face_direction]
        #logger.debug(f"Texture: {self.texture}")
        #self.sprite = Sprite(self.texture)


    @debounce(.1)
    def face_left(self):
        self.character_face_direction = LEFT_FACING
        self.node.angle = 45

    @debounce(.1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING
        self.node.angle = -45

    def update(self, delta_time: float = 1/60):
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

        #self.texture = self.walk_textures[self.cur_texture * 2 + self.character_face_direction]
        #self.sprite.texture = self.texture
        self.sprite = self.walk_textures[self.cur_texture * 2 + self.character_face_direction]
