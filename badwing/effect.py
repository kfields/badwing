import random

import arcade

from badwing.constants import *
from badwing.particle import AnimatedAlphaParticle

class Effect(arcade.Sprite):
    def __init__(self, position=(0,0)):
        super().__init__(center_x=position[0], center_y=position[1])
        #self.position = position

    def setup(self):
        pass

    def update(self, delta_time=1/60):
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
