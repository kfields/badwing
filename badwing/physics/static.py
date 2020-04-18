import arcade
import pymunk

from badwing.constants import *
from badwing.physics import Physics, PhysicsMeta

class StaticPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_STATIC)

    def setup():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model):
        sprite = model.sprite
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pymunk.Vec2d(sprite.center_x, sprite.center_y)
        return body
