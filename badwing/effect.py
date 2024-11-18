import random

import glm

from crunge.engine import Renderer
from crunge.engine.d2.sprite import SpriteVu

from badwing.constants import *

# from badwing.particle import AnimatedAlphaParticle


class Effect(SpriteVu):
    def __init__(self, position=glm.vec2()):
        super().__init__(center_x=position[0], center_y=position[1])
        # self.position = position


class EffectList:
    def __init__(self, effects=[]):
        self.effects = effects

    def append(self, effect):
        self.effects.append(effect)

    def draw(self, renderer: Renderer):
        for e in self.effects:
            e.draw()

    def update(self, delta_time):
        for e in self.effects:
            e.update(delta_time)
