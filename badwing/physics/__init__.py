import arcade
import pymunk

import badwing.app
from badwing.constants import *

class Physics:
    def __init__(self):
        pass
    def setup():
        pass

    def update(self, delta_time=1/60.0):
        pass

class PhysicsEngine:
    def __init__(self, gravity=GRAVITY, iterations=35):
        badwing.app.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations
    
    def setup():
        pass

    def update(self, delta_time=1/60.0):
        self.space.step(delta_time)
