import pymunk

from crunge.engine import Base

import badwing.app
from badwing.constants import *


class PhysicsEngine(Base):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
        badwing.app.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations

    def update(self, delta_time=1 / 60.0):
        self.space.step(delta_time)
