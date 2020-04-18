import math
import random
import arcade
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

import badwing.app
from badwing.constants import *
import badwing.geom
from badwing.model import ModelFactory, DynamicModel

class Obstacle(DynamicModel):
    def __init__(self, position, sprite, geom):
        super().__init__(position, sprite, geom=geom)

    @classmethod
    def create(self, sprite):
        kind = sprite.properties['type']
        model = kinds[kind].create(sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model

BOX_MASS = 1
BALL_MASS = 1
ROCK_MASS = 1

class Box(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, geom=badwing.geom.BoxGeom)
        self.mass = BOX_MASS

    @classmethod
    def create(self, sprite):
        return Box(sprite.position, sprite)

class Ball(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, geom=badwing.geom.BallGeom)
        self.mass = BALL_MASS

    @classmethod
    def create(self, sprite):
        return Ball(sprite.position, sprite)


class Rock(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, badwing.geom.HullGeom)

    @classmethod
    def create(self, sprite):
        return Rock(sprite.position, sprite)

class ObstacleFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        for sprite in self.layer.sprites:
            model = Obstacle.create(sprite)
            self.layer.add_model(model)


kinds = {
    'block': Box,
    'boxCrate': Box,
    'boxCrate_double': Box,
    'Ball': Ball,
    'RockBig1': Rock
}