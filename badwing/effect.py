import random

import arcade

from badwing.constants import *
from badwing.particle import AnimatedAlphaParticle

#TODO:  Seems like it should be called Firework to me
class Effect:
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

class EffectList:
    def __init__(self, effects=[]):
        self.effects = effects

    def append(self, effect):
        self.effects.append(effect)

    def draw(self):
        for e in self.effects:
            e.draw()

    def update(self, delta_time):
        for e in self.effects:
            e.update(delta_time)
