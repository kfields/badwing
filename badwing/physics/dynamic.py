import arcade
import pymunk

from badwing.constants import *
from badwing.physics import Physics
class DynamicPhysics(Physics):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
