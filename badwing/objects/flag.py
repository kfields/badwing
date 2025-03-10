from crunge.engine.d2.node_2d import Node2D

from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce
#from badwing.model import Model, Group
#from badwing.model_factory import ModelFactory
from badwing.tile import TileLayer

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32

MOVEMENT_SPEED = 5
FRAMES = 10
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

RATE_DELTA = 1/60
RATE_MIN = 0
RATE_MAX = .1

class Pole(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)
        self.collected = False

class Flag(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)
        self.collected = False

    @classmethod
    def produce(self, position, sprite):
        kind = sprite.properties['class']
        node = kinds[kind].produce(position, sprite)
        return node

    def collect(self):
        if self.collected:
            return True
        self.collected = collected = True
        #TODO: not working as planned
        old_sprite = self.sprite
        self.sprite = sprite = arcade.Sprite()
        sprite.texture = old_sprite.texture
        old_sprite.remove_from_sprite_lists()
        return collected


class FlagGreen(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagGreen(position, sprite)

class FlagYellow(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagYellow(position, sprite)

class FlagRed(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagRed(position, sprite)

kinds = {
    'Pole': Pole,
    'FlagGreen': FlagGreen,
    'FlagYellow': FlagYellow,
    'FlagRed': FlagRed,
}

'''
class FlagFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def produce(self):
        for sprite in self.layer.sprites:
            print("sprite.properties: ", sprite.properties)
            kind = sprite.properties['class']
            if kind == 'Pole':
                node = Pole(sprite.position, sprite)
            else:
                node = Flag.produce(sprite.position, sprite)
            self.layer.add_node(node)
'''