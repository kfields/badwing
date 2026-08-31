import glm

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import Geom, BoxGeom, BallGeom, HullGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu

from badwing.constants import *


class Obstacle(DynamicEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, model=sprite)

    @classmethod
    def produce(cls: type["Obstacle"], kind: str, position: glm.vec2, sprite: Sprite):
        node = kinds[kind](position, sprite)
        return node


class Box(Obstacle):
    geom = BoxGeom()

    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite)


class Ball(Obstacle):
    geom = BallGeom()

    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite)


class Rock(Obstacle):
    geom = HullGeom()

    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, sprite)


kinds = {
    "block": Box,
    "boxCrate": Box,
    "boxCrate_double": Box,
    "Ball": Ball,
    "RockBig1": Rock,
}
