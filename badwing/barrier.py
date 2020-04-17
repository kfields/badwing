import arcade
import pymunk

from badwing.constants import *
from badwing.layer import Layer
from badwing.model import StaticModel

BARRIER_WIDTH = 100
BARRIER_HEIGHT = 1000

class Barrier(StaticModel):
    def __init__(self, left, bottom, right, top):
        super().__init__(None)
        self.width = width = right - left
        self.height = height = top - bottom
        self.position = (left + width/2, bottom + height/2)

    def create_body(self):
        self.body = body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pymunk.Vec2d(self.position[0], self.position[1])

    def create_shapes(self):
        shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        shape.friction = 10
        self.shapes.append(shape)

class BarrierLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.barrier_width = BARRIER_WIDTH
        self.barrier_height = self.height
        self.left_barrier = None
        self.right_barrier = None
        
    def setup(self):
        super().setup()
        left, bottom, right, top = self.level.left, self.level.bottom, self.level.right, self.level.top
        self.top_barrier = top_barrier = Barrier(left - self.barrier_width, top + BARRIER_HEIGHT, right, top)
        self.left_barrier = left_barrier = Barrier(left - self.barrier_width, bottom, left, self.height)
        self.right_barrier = right_barrier = Barrier(right, bottom, right + self.barrier_width, self.height)
        self.add_model(top_barrier)
        self.add_model(left_barrier)
        self.add_model(right_barrier)
