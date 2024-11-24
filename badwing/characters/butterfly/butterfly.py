import random

from loguru import logger
import glm

from crunge.engine.math import Bounds2
from crunge.engine.d2.sprite import SpriteVuGroup

from crunge.engine.d2.entity import Entity2D, EntityGroup2D

from badwing.assets import asset
from badwing.constants import *
from badwing.util import debounce
from badwing.model_factory import ModelFactory

from badwing.characters.butterfly.butterfly_brain import ButterflyBrain
from badwing.characters.butterfly.butterfly_vu import ButterflyVu

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32
CHARACTER_SCALING = 1

MOVEMENT_SPEED = 5
FRAMES = 10
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

RATE_DELTA = 1/60
RATE_MIN = 0
RATE_MAX = .1

RANGE = 512 # How far they can travel
HALF_RANGE = RANGE/2

class Butterfly(Entity2D):
    def __init__(self, position=glm.vec2(), vu=None, border=Bounds2(0,0,640,480)):
        super().__init__(position, vu=vu, brain=ButterflyBrain(self))
        self.border = border

    @classmethod
    def produce(self, kind, position=glm.vec2(), border=Bounds2(0,0,640,480)):
        model = kinds[kind].produce(position, border)
        return model

    @classmethod
    def create_from(self, sprite):
        kind = sprite.properties['class']
        pos = sprite.position
        border = Bounds2(pos[0]-HALF_RANGE, pos[1]-HALF_RANGE, pos[0]+HALF_RANGE, pos[1]+HALF_RANGE)
        model = kinds[kind].produce(pos, border)
        return model

class ButterflyAqua(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(8).create()
        return ButterflyAqua(position, sprite, border)

class ButterflyBlue(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(0).create()
        return ButterflyBlue(position, sprite, border)

class ButterflyBrown(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(4).create()
        return ButterflyBrown(position, sprite, border)

class ButterflyCyan(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(5).create()
        return ButterflyCyan(position, sprite, border)

class ButterflyGreen(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(1).create()
        return ButterflyGreen(position, sprite, border)

class ButterflyIridescent(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(6).create()
        return ButterflyIridescent(position, sprite, border)

class ButterflyRed(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(7).create()
        return ButterflyRed(position, sprite, border)

class ButterflyTan(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(3).create()
        return ButterflyTan(position, sprite, border)

class ButterflyTeal(Butterfly):
    @classmethod
    def produce(self, position, border=Bounds2(0,0,640,480)):
        sprite = ButterflyVu(2).create()
        return ButterflyTeal(position, sprite, border)


kinds = {
    'ButterflyBlue': ButterflyBlue,
    'ButterflyAqua': ButterflyAqua,
    'ButterflyBrown': ButterflyBrown,
    'ButterflyCyan': ButterflyCyan,
    'ButterflyGreen': ButterflyGreen,
    'ButterflyIridescent': ButterflyIridescent,
    'ButterflyRed': ButterflyRed,
    'ButterflyTan': ButterflyTan,
    'ButterflyTeal': ButterflyTeal
}

kinds_list = list(kinds)

class Butterflies(EntityGroup2D):
    def __init__(self, border=Bounds2(0,0,640,480)):
        super().__init__()

    @classmethod
    def create_random(self, count, border=Bounds2(0,0,640,480)):
        group = Butterflies()
        for i in range(count):
            center_x = random.randint(0, border.right)
            center_y = random.randint(0, border.top)
            position = glm.vec2(center_x, center_y)
            logger.debug(f'position: {position}')
            ndx = random.randint(0, 8)
            kind = kinds_list[ndx]
            butterfly = Butterfly.produce(kind, position, border)
            group.add_model(butterfly)
        return group

class ButterflyFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def produce(self):
        orig_sprites = self.layer.sprites
        self.layer.sprites = SpriteVuGroup()

        for sprite in orig_sprites:
            #print(sprite)
            kind = sprite.properties.get('class')
            if not kind:
                continue
            position = sprite.position
            model = Butterfly.create_from(sprite)
            #print(model)
            self.layer.add_model(model)
