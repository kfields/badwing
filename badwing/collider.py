import arcade
import math
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from badwing.constants import *


class ColliderMeta(type):

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class Collider():
    def __init__(self, kind):
        self.type = kind

    def create_shapes(self, model):
        pass

class GroupCollider(Collider, metaclass=ColliderMeta):
    def __init__(self, kind=CT_GROUP):
        super().__init__(kind)

class PolyCollider(Collider):
    def __init__(self, kind):
        super().__init__(kind)

class DecomposedCollider(PolyCollider, metaclass=ColliderMeta):
    def __init__(self):
        super().__init__(CT_DECOMPOSED)

    def create_shapes(self, model):
        sprite = model.sprite
        body = model.body
        position = model.position
        transform=model.transform

        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        #print(points)
        polys = convex_decomposition(sprite.points, 0)
        #print(polys)
        for poly in polys:
            points = [i - center for i in poly ]
            #print(points)
            shape = pymunk.Poly(body, points, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = model.physics.type
            shapes.append(shape)
        return shapes

class HullCollider(PolyCollider, metaclass=ColliderMeta):
    def __init__(self):
        super().__init__(CT_HULL)

    def create_shapes(self, model):
        sprite = model.sprite
        body = model.body
        position = model.position
        transform=model.transform

        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        #print(points)
        poly = to_convex_hull(sprite.points, .01)
        #print(poly)
        points = [i - center for i in poly ]
        #print(points)
        shape = pymunk.Poly(body, points, transform)
        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = model.physics.type
        shapes.append(shape)
        return shapes
