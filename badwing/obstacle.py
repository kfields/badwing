import glm

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import Geom, BoxGeom, BallGeom, HullGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu

import badwing.globe
from badwing.constants import *


class Obstacle(DynamicEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite, geom: Geom):
        super().__init__(position, vu=SpriteVu(), model=sprite, geom=geom)

    @classmethod
    def produce(cls: type["Obstacle"], kind: str, position: glm.vec2, sprite: Sprite):
        node = kinds[kind](position, sprite)
        return node


BOX_MASS = 50.0
BALL_MASS = 50.0
ROCK_MASS = 50.0


class Box(Obstacle):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite, geom=BoxGeom())
        self.mass = BOX_MASS


class Ball(Obstacle):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite, geom=BallGeom())
        self.mass = BALL_MASS


class Rock(Obstacle):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite, geom=HullGeom())
        self.mass = ROCK_MASS


kinds = {
    "block": Box,
    "boxCrate": Box,
    "boxCrate_double": Box,
    "Ball": Ball,
    "RockBig1": Rock,
}
