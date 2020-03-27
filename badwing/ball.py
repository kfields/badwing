import math
import pymunk

from badwing.assets import asset
from badwing.model import Model


class Ball(Model):
    def __init__(self, sprite, position=(256, 512)):
        super().__init__(sprite)
        mass = 1
        radius = 11
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = position
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        badwing.app.level.space.add(body, shape)
        self.body = body

    @classmethod
    def create(self):
        img_src = asset("items/coinGold.png")
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Ball(sprite)
