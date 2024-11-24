import math
import random

from loguru import logger

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite.sprite_atlas_loader import SpriteAtlasLoader

from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce


SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32
CHARACTER_SCALING = 1

MOVEMENT_SPEED = 5
FRAMES = 10
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

RATE_DELTA = 1 / 60
RATE_MIN = 0
RATE_MAX = 0.1

RANGE = 512  # How far they can travel
HALF_RANGE = RANGE / 2


class ButterflyVu(SpriteVu):
    def __init__(self, index):
        super().__init__()

        self.change_x = 0
        self.change_y = 0
        
        # Animation timing
        self.time = 1
        self.update_time = 0
        self.rate = 1 / 60
        self.angle = -45
        self.character_face_direction = RIGHT_FACING
        # Used for flipping between image sequences
        self.current_sprite_index = 0

        # self.scale = CHARACTER_SCALING

        # --- Load Textures ---
        sprite_rects = []
        for i in range(FRAMES):
            sprite_rects.append(
                Rect2i(
                    i * SPRITE_WIDTH * 2,
                    index * SPRITE_HEIGHT,
                    SPRITE_WIDTH,
                    SPRITE_HEIGHT,
                )
            )
            sprite_rects.append(
                Rect2i(
                    i * SPRITE_WIDTH * 2 + SPRITE_WIDTH,
                    index * SPRITE_HEIGHT,
                    SPRITE_WIDTH,
                    SPRITE_HEIGHT,
                )
            )

        self.sprites = SpriteAtlasLoader().load(
            asset("sprites/butterflies.png"), sprite_rects, name=f"butterflies{index}"
        )
        self.idle_sprite_pair = [self.sprites[0], self.sprites[1]]
        self.sprite = self.idle_sprite_pair[self.character_face_direction]

    @debounce(0.1)
    def face_left(self):
        self.character_face_direction = LEFT_FACING
        self.node.angle = 45

    @debounce(0.1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING
        self.node.angle = -45

    def update(self, delta_time: float = 1 / 60):
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
            self.texture = self.idle_sprite_pair[self.character_face_direction]
            return
        # Walking animation
        self.current_sprite_index += 1

        if self.current_sprite_index > FRAMES - 1:
            self.current_sprite_index = 0

        # self.texture = self.walk_textures[self.cur_texture * 2 + self.character_face_direction]
        # self.sprite.texture = self.texture
        self.sprite = self.sprites[
            self.current_sprite_index * 2 + self.character_face_direction
        ]
