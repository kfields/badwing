from crunge.engine.d2.entity import DynamicEntity2D

import badwing.app
from badwing.constants import *
#import badwing.geom
#from badwing.model import DynamicModel
from badwing.model_factory import ModelFactory

class Obstacle(DynamicEntity2D):
    def __init__(self, position, sprite, geom):
        super().__init__(position, sprite, geom=geom)

    @classmethod
    def produce(self, sprite):
        print("sprite.properties: ", sprite.properties)
        kind = sprite.properties['class']
        node = kinds[kind].produce(sprite)
        #print(model)
        #print(vars(sprite))
        #print(kind)
        #print(sprite.points)
        return node

BOX_MASS = 1
BALL_MASS = 1
ROCK_MASS = 1

class Box(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, geom=badwing.geom.BoxGeom)
        self.mass = BOX_MASS

    @classmethod
    def produce(self, sprite):
        return Box(sprite.position, sprite)

class Ball(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, geom=badwing.geom.BallGeom)
        self.mass = BALL_MASS

    @classmethod
    def produce(self, sprite):
        return Ball(sprite.position, sprite)


class Rock(Obstacle):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, badwing.geom.HullGeom)

    @classmethod
    def produce(self, sprite):
        return Rock(sprite.position, sprite)

class ObstacleFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def produce(self):
        for sprite in self.layer.sprites:
            node = Obstacle.produce(sprite)
            self.layer.add_node(node)


kinds = {
    'block': Box,
    'boxCrate': Box,
    'boxCrate_double': Box,
    'Ball': Ball,
    'RockBig1': Rock
}