from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom, BallGeom, HullGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu

import badwing.globe
from badwing.constants import *


class Obstacle(DynamicEntity2D):
    def __init__(self, position, sprite, geom):
        super().__init__(position, vu=SpriteVu(), model=sprite, geom=geom)

    @classmethod
    def produce(self, kind, position, sprite):
        node = kinds[kind].produce(position, sprite)
        return node


BOX_MASS = 1
BALL_MASS = 1
ROCK_MASS = 1


class Box(Obstacle):
    def __init__(self, position, sprite=None):
        super().__init__(position, sprite, geom=BoxGeom())
        self.mass = BOX_MASS

    @classmethod
    def produce(self, position, sprite):
        return Box(position, sprite)


class Ball(Obstacle):
    def __init__(self, position, sprite=None):
        super().__init__(position, sprite, geom=BallGeom())
        self.mass = BALL_MASS

    @classmethod
    def produce(self, sprite):
        return Ball(sprite.position, sprite)


class Rock(Obstacle):
    def __init__(self, position=(0, 0), sprite=None):
        super().__init__(position, sprite, geom=HullGeom())

    @classmethod
    def produce(self, sprite):
        return Rock(sprite.position, sprite)


kinds = {
    "block": Box,
    "boxCrate": Box,
    "boxCrate_double": Box,
    "Ball": Ball,
    "RockBig1": Rock,
}
