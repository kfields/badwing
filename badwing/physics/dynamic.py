import arcade
import pymunk

from badwing.constants import *
from badwing.physics import Physics, PhysicsMeta, PhysicsEngine

class DynamicPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_DYNAMIC)

    def setup():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

class DynamicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
