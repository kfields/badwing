import arcade
import pymunk

from badwing.constants import *

class PhysicsEngine:
    def __init__(self, gravity=GRAVITY, iterations=35):
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations
    
    def setup():
        pass

    def update(self):
        pass
