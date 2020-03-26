import math
import random
import arcade
import pymunk

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
        return model

BOX_MASS = 1
BOX_WIDTH = 128
ROCK_MASS = 1

class BoxCrateDouble(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        print(sprite.position)
        print(position)
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        self.shape = shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2

    @classmethod
    def create(self, sprite):
        return BoxCrateDouble(sprite, position=(sprite.center_x, sprite.center_y))


class RockBig1(Obstacle):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = BOX_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        self.shape = shape = pymunk.Poly(body, sprite.points)
        shape.friction = 10
        shape.elasticity = 0.2

    @classmethod
    def create(self, sprite):
        return RockBig1(sprite, position=(sprite.center_x, sprite.center_y))


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