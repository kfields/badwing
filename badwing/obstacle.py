import math
import random
import arcade
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull
import badwing.app
from badwing.constants import *
from badwing.model import DynamicModel
from badwing.tile import DynamicTileLayer

class Obstacle(DynamicModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, sprite):
        kind = sprite.properties['type']
        model = kinds[kind].create(sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model

BOX_MASS = 1
BOX_WIDTH = 128
ROCK_MASS = 1

class BoxCrate(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        self.position = position
        self.width = sprite.texture.width * TILE_SCALING
        self.height = sprite.texture.height * TILE_SCALING

    def create_body(self):
        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = self.position

    def create_shapes(self):
        shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        shape.friction = 10
        shape.elasticity = 0.2
        self.shapes.append(shape)

    @classmethod
    def create(self, sprite):
        return BoxCrate(sprite, position=(sprite.center_x, sprite.center_y))


class Rock(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        self.position = position
        self.width = sprite.texture.width * TILE_SCALING
        self.height = sprite.texture.height * TILE_SCALING

    def create_body(self):
        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        #moment = pymunk.moment_for_poly(mass, points)
        self.body = body = pymunk.Body(mass, moment)
        body.position = self.position

    def create_shapes(self):
        center = Vec2d(self.position)
        points = self.sprite.points
        #print(points)
        polys = convex_decomposition(self.sprite.points, 0)
        #polys = to_convex_hull(sprite.points, .01)
        #print(polys)

        for poly in polys:
            #print(poly)
            #points = [(i.x, i.y) for i in poly ]
            points = [i - center for i in poly ]
            #print(points)
            shape = pymunk.Poly(self.body, points)
            shape.friction = 10
            shape.elasticity = 0.2
            self.shapes.append(shape)

    @classmethod
    def create(self, sprite):
        return Rock(sprite, position=(sprite.center_x, sprite.center_y))

class ObstacleTileLayer(DynamicTileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            model = Obstacle.create(sprite)
            self.add_model(model)

kinds = {
    'block': BoxCrate,
    'boxCrate': BoxCrate,
    'boxCrate_double': BoxCrate,
    'RockBig1': Rock
}