import arcade
import pymunk

from badwing.constants import *
from badwing.physics import Physics, PhysicsEngine

class DynamicPhysics(Physics):
    def __init__(self):
        pass
    def setup():
        pass

    def update(self, delta_time=1/60.0):
        pass

class DynamicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
