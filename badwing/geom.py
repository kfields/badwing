import arcade
import math
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from badwing.constants import *


class GeomMeta(type):

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class Geom():
    def __init__(self, kind):
        self.type = kind

    def create_shapes(self, model, transform=None):
        pass

class BoxGeom(Geom, metaclass=GeomMeta):
    def __init__(self):
        super().__init__(GT_BOX)

    def get_moment(self, model):
        return pymunk.moment_for_box(model.mass, (model.width, model.height))

    def create_shapes(self, model, transform=None):
        shapes = []
        shape = pymunk.Poly.create_box(model.body, (model.width, model.height))
        shape.friction = 10
        shape.elasticity = 0.2
        shapes.append(shape)
        return shapes

class BallGeom(Geom, metaclass=GeomMeta):
    def __init__(self):
        super().__init__(GT_BALL)

    def get_moment(self, model):
        return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))

    def create_shapes(self, model, transform=None):
        shapes = []
        shape = pymunk.Circle(model.body, model.radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        shapes.append(shape)
        return shapes

class GroupGeom(Geom, metaclass=GeomMeta):
    def __init__(self, kind=GT_GROUP):
        super().__init__(kind)

    def create_shapes(self, model):
        return []
        
    def get_moment(self, model):
        return pymunk.moment_for_box(model.mass, (model.width, model.height))

class PolyGeom(Geom):
    def __init__(self, kind):
        super().__init__(kind)

    def get_moment(self, model):
        return pymunk.moment_for_box(model.mass, (model.width, model.height))
        #return pymunk.moment_for_poly(model.mass, model.sprite.points, (-32,-32))
        #return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))

SLOP = 0.01
class DecomposedGeom(PolyGeom, metaclass=GeomMeta):
    def __init__(self):
        super().__init__(GT_DECOMPOSED)

    def create_shapes(self, model, transform=None):
        if not transform:
            transform = model.transform

        sprite = model.sprite
        body = model.body
        position = model.position

        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.get_hit_box()
        #print(points)
        polys = convex_decomposition(points, SLOP)
        #print(polys)
        for poly in polys:
            shape = pymunk.Poly(body, poly, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = model.physics.type
            shapes.append(shape)
        return shapes

class HullGeom(PolyGeom, metaclass=GeomMeta):
    def __init__(self):
        super().__init__(GT_HULL)

    def create_shapes(self, model, transform=None):
        if not transform:
            transform = model.transform
        #print('transform', transform)
        sprite = model.sprite
        body = model.body
        position = model.position
        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.get_hit_box()
        #print(model.__class__)
        #print(points)
        points = to_convex_hull(points, SLOP)
        #print(points)
        shape = pymunk.Poly(body, points, transform)

        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = model.physics.type
        shapes.append(shape)
        return shapes
