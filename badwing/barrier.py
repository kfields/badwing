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
        width = right - left
        height = top - bottom
        center_x = left + width/2
        center_y = bottom + height/2

        self.body = body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pymunk.Vec2d(center_x, center_y)

        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        self.shapes.append(shape)


class BarrierLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.left_barrier = None
        self.right_barrier = None
        
    def setup(self):
        super().setup()
        left, bottom, right, top = self.level.left, self.level.bottom, self.level.right, self.level.top
        self.left_barrier = left_barrier = Barrier(left - BARRIER_WIDTH, bottom, left, BARRIER_HEIGHT)
        self.right_barrier = right_barrier = Barrier(right, bottom, right + BARRIER_WIDTH, BARRIER_HEIGHT)
        self.add_model(left_barrier)
        self.add_model(right_barrier)
