import math
import glm
import pymunk
from pymunk import Vec2d
import arcade

from badwing.constants import *
from badwing.assets import asset
from badwing.model import DynamicModel

BOX_MASS = 1
BOX_WIDTH = 128

class Box(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2
        self.shapes.append(shape)

    @classmethod
    def create(self, position=(492, 192)):
        img_src = asset("tiles/boxCrate_double.png")
        #sprite = arcade.Sprite(img_src, CHARACTER_SCALING, image_width=CHASSIS_WIDTH, image_height=CHASSIS_HEIGHT)
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Box(sprite, position)
