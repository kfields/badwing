import math
import random

from loguru import logger
import glm

import badwing.globe
from badwing.brain import Brain

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite.sprite_atlas_loader import SpriteAtlasLoader

from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32

FRAMES = 10
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

RATE_DELTA = 1 / 60
RATE_MIN = 0
RATE_MAX = 0.1

DEG_RADS = (math.pi*2)/360


def distance2d(start, end):
    diffX = start.x - end.x
    diffY = start.y - end.y
    return math.sqrt((diffX*diffX)+(diffY*diffY))    

class ButterflyBrain(Brain):
    def __init__(self, index: int):
        super().__init__()
        self.heading = random.randint(0, 359)
        self.wheel = 0
        self.begin_pos = glm.vec2()
        self.end_pos = glm.vec2()
        self.sensor_range = 512

        # Animation timing
        self.time = 1
        self.update_time = 0
        self.rate = 1 / 60
        #self.angle = -45
        self.character_face_direction = RIGHT_FACING
        # Used for flipping between image sequences
        self.current_sprite_index = 0

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

    def _create(self):
        self.node.angle = -45
        self.sprite = self.idle_sprite_pair[self.character_face_direction]

    def update(self, delta_time):
        super().update(delta_time)
        if(self.at_goal()):
            pt = random.randint(0, 3)
            pd = random.randint(0, 359)
            if(pt == 0):
                self.left(pd)
            elif(pt == 2):
                self.right(pd)
            self.randforward()
        self.move()

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
        if self.velocity.x < 0 and self.character_face_direction == RIGHT_FACING:
            self.face_left()
        elif self.velocity.x > 0 and self.character_face_direction == LEFT_FACING:
            self.face_right()

        # Idle animation
        if self.velocity.x == 0 and self.velocity.y == 0:
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

    def at_goal(self):
        distance = distance2d(self.position, self.end_pos)
        return distance < 5

    def move_to(self, end_pos):
        self.begin_pos = self.position
        self.end_pos = end_pos

    def move(self):
        x, y = self.position
        to_x, to_y = self.end_pos

        pd = random.randint(0, 3)
        if(pd == 0):
            self.micro_left()
        elif(pd == 2):
            self.micro_right()

        steering_ndx = int(math.pi+(math.atan2(y - to_y, x - to_x)))
        delta = steering[steering_ndx][self.wheel]

        self.try_move(delta)

    def try_move(self, delta):
        #return
        delta_x, delta_y = delta
        next_x, next_y = 0, 0
        need_turn = False

        bounds = self.node.bounds
        #logger.debug(f"Bounds: {bounds}")
        min_x, min_y, max_x, max_y = bounds.left, bounds.bottom, bounds.right, bounds.top
        border  = self.node.border
        #logger.debug(f"Border: {border}")
        w_min_x, w_min_y, w_max_x, w_max_y = border.left, border.bottom, border.right, border.top

        if(min_x < w_min_x):
            delta_x = w_min_x - min_x
            need_turn = True
        elif(max_x > w_max_x):
            delta_x = w_max_x - max_x
            need_turn = True

        if(min_y < w_min_y):
            delta_y = w_min_y - min_y
            need_turn = True
        elif(max_y > w_max_y):
            delta_y = w_max_y - max_y
            need_turn = True
        
        #TODO:use pymunk
        
        if not need_turn:
            ground_layer = badwing.globe.scene.ground_layer
            if ground_layer:
                need_turn = collision_list = arcade.check_for_collision_with_list(self.sprite, ground_layer.sprites)

        if(need_turn):
            self.right(45)
            self.randforward()

        pos = self.position
        next_x = pos.x + delta_x
        next_y = pos.y + delta_y                    
        
        self.position = glm.vec2(next_x, next_y)
        #sprite = self.node.vu
        #sprite.change_x = pos.x - next_x
        #sprite.change_y = pos.y - next_y
        self.velocity = glm.vec2(pos.x - next_x, pos.y - next_y)

    def left(self, angle):
        heading = self.heading - angle
        self.heading = heading if heading > 0 else 360 + heading

    def right(self, angle):
        heading = self.heading + angle
        self.heading = heading if heading < 359 else heading - 360

    def micro_left(self):
        ph = self.wheel - 1
        if(ph < 0 ):
            ph = 0
        self.wheel = ph

    def micro_right(self):
        ph = self.wheel + 1
        if(ph > 2):
            ph = 2
        self.wheel = ph

    def forward(self, distance):
        x, y = self.position
        px = x+(distance*(math.cos(self.heading*DEG_RADS)))
        py = y+(distance*(math.sin(self.heading*DEG_RADS)))
        self.move_to(glm.vec2(px, py))

    def randforward(self):
        self.forward(random.randint(0, self.sensor_range))

    @debounce(0.1)
    def face_left(self):
        self.character_face_direction = LEFT_FACING
        self.node.angle = 45

    @debounce(0.1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING
        self.node.angle = -45

steering = [
    [(1, -1), (1, 0), (1, 1)],
    [(1, 0), (1, 1), (0, 1)],
    [(1, 1), (0, 1), (-1, 1)],
    [(0, 1), (-1, 1), (-1, 0)],
    [(-1, 1), (-1, 0), (-1, -1)],
    [(-1, 0), (-1, -1), (0, -1)],
    [(-1, -1), (0, -1), (1, -1)],
    [(0, -1), (1, -1), (1, 0)]
]
