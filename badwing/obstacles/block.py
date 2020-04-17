import math
import random
import arcade
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull
import badwing.app
from badwing.constants import *
from badwing.model import DynamicModel
from badwing.tile import DynamicTileLayer

BOX_MASS = 1
BOX_WIDTH = 128

class BoxCrate(Obstacle):
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
    def create(self, sprite):
        return BoxCrate(sprite, position=(sprite.center_x, sprite.center_y))
