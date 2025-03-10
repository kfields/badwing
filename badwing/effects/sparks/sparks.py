import glm

from crunge.engine.d2.node_2d import Node2D

from .sparks_vu import SparksVu

class Sparks(Node2D):
    def __init__(self, position: glm.vec2, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)) -> None:
        super().__init__(position, vu=SparksVu(color))
