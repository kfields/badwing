import math

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

    def create_body(self, model, offset=None):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.model = model
        body.position = model.position
        body.angle = math.radians(model.angle)
        return body
