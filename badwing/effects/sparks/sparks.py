import glm

from crunge.engine.d2.node_2d import Node2D

from .sparks_vu import SparksVu


class Sparks(Node2D):
    def __init__(self, position: glm.vec2, color: glm.vec4 = None) -> None:
        if color is None:
            color = glm.vec4(0.0, 0.0, 1.0, 1.0)
        super().__init__(position, scale = glm.vec2(0.005, 0.005))
        self.color = color

    def _seat(self) -> None:
        self.add(SparksVu(self.color))
        super()._seat()

"""
class Sparks(Node2D):
    def __init__(self, position: glm.vec2, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)) -> None:
        super().__init__(position, scale=glm.vec2(0.005, 0.005), vu=SparksVu(color))
"""