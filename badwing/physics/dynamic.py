import arcade
import pymunk

from badwing.constants import *
from badwing.physics import PhysicsEngine
class DynamicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
