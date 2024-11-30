import sys
import os

from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.math import Bounds2
#from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics import PhysicsEngine2D

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level
from badwing.controller import Controller

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.characters.butterfly import Butterflies


class StartScene(Level):
    def __init__(self, name, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)


    @classmethod
    def produce(self):
        level = StartScene()
        return level
        
    def get_next_level(self):
        import badwing.scenes.level1
        return badwing.scenes.level1.Level1

    def _create(self):
        super()._create()
        self.add_layer(BarrierLayer(self, 'barrier'))

        self.add_layer(BackgroundLayer(self, 'background', ":resources:/backgrounds/backgroundColorGrass.png"))
        self.butterfly_layer = butterfly_layer = SceneLayer(self, 'butterflies')
        butterflies = Butterflies.create_random(20, Bounds2(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        #butterflies = Butterflies.create_random(20, Bounds2(0,0,self.width, self.height))
        self.butterfly_layer.attach(butterflies)
        self.add_layer(butterfly_layer)

    '''
    def update(self, delta_time):
        super().update(delta_time)
        self.physics_engine.update()
    '''