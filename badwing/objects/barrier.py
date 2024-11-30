import glm

from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.physics.geom import BoxGeom

from badwing.constants import *
from badwing.scene_layer import SceneLayer

BARRIER_WIDTH = 100
BARRIER_HEIGHT = 1000

class Barrier(StaticEntity2D):
    def __init__(self, left, bottom, right, top):
        width = right - left
        height = top - bottom
        position = glm.vec2(left + width/2, bottom + height/2)
        super().__init__(position, glm.vec2(width, height), geom=BoxGeom)


class BarrierLayer(SceneLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.barrier_width = BARRIER_WIDTH
        self.barrier_height = self.scene.height
        self.left_barrier = None
        self.right_barrier = None
        
    def _create(self):
        super()._create()
        left, bottom, right, top = self.level.left, self.level.bottom, self.level.right, self.level.top
        self.top_barrier = top_barrier = Barrier(left - self.barrier_width, top + BARRIER_HEIGHT, right, top)
        self.left_barrier = left_barrier = Barrier(left - self.barrier_width, bottom, left, top)
        self.right_barrier = right_barrier = Barrier(right, bottom, right + self.barrier_width, top)

        self.attach(top_barrier)
        self.attach(left_barrier)
        self.attach(right_barrier)
