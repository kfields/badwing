import math

import glm
import pymunk
from pymunk.vec2d import Vec2d

from badwing.constants import *
from badwing.physics import Physics, PhysicsMeta, PhysicsEngine

class DynamicPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_DYNAMIC)

    def _create():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        mass = model.mass
        #moment = pymunk.moment_for_box(mass, (self.width, self.height))
        moment = model.geom.get_moment(model)
        body = pymunk.Body(mass, moment)
        body.model = model

        if offset:
            #print('offset', offset)
            position = glm.vec2(model.position.x + offset[0], model.position.y + offset[1])

        else:
            position = model.position
        body.position = tuple(position)
        body.angle = math.radians(model.angle)
        return body

class DynamicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
