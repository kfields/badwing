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
        kind = sprite.properties['kind']
        model = kinds[kind].create(sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return model

BOX_MASS = 1
BOX_WIDTH = 128
ROCK_MASS = 1

class BoxCrateDouble(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2
        self.shapes.append(shape)

    @classmethod
    def create(self, sprite):
        return BoxCrateDouble(sprite, position=(sprite.center_x, sprite.center_y))


class RockBig1(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        center = Vec2d(position)
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        points = sprite.points
        #print(points)

        polys = convex_decomposition(sprite.points, 0)
        #polys = to_convex_hull(sprite.points, .01)
        #print(polys)


        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        #moment = pymunk.moment_for_poly(mass, points)
        self.body = body = pymunk.Body(mass, moment)
        body.position = position
        #print('ROCK')
        for poly in polys:
            #print(poly)
            #points = [(i.x, i.y) for i in poly ]
            points = [i - center for i in poly ]
            #print(points)
            shape = pymunk.Poly(body, points)
            shape.friction = 10
            shape.elasticity = 0.2
            self.shapes.append(shape)        

    @classmethod
    def create(self, sprite):
        return RockBig1(sprite, position=(sprite.center_x, sprite.center_y))
    '''
    def update(self, delta_time):
        super().update(delta_time)
        print(self.position)
    '''
class ObstacleTileLayer(DynamicTileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            model = Obstacle.create(sprite)
            self.add_model(model)

'''
class ObstacleObjectLayer(DynamicTileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        self.sprites = arcade.SpriteList()
        for orig_sprite in orig_sprites:
            #print(vars(orig_sprite))
            #print(orig_sprite.properties)
            model = Butterfly.create(orig_sprite)
            self.sprites.append(model.sprite)
            self.add_model(model)
'''

kinds = {
    'BoxCrateDouble': BoxCrateDouble,
    'RockBig1': RockBig1
}