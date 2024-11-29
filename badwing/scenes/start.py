import sys
import os

from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.math import Bounds2
from crunge.engine.d2.physics import DynamicPhysicsEngine

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
    def __init__(self, name='start'):
        super().__init__(name)
        # Our physics engine
        self.physics_engine = physics_engine = DynamicPhysicsEngine().create()
        self.space = physics_engine.space

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0


    @classmethod
    def produce(self):
        level = StartScene()
        return level
        
    def get_next_level(self):
        import badwing.scenes.level1
        return badwing.scenes.level1.Level1

    def _create(self):
        super()._create()
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        self.add_layer(BarrierLayer(self, 'barrier'))

        self.add_layer(BackgroundLayer(self, 'background', ":resources:/backgrounds/backgroundColorGrass.png"))
        self.butterfly_layer = butterfly_layer = SceneLayer(self, 'butterflies')
        butterflies = Butterflies.create_random(20, Bounds2(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        self.butterfly_layer.attach(butterflies)
        self.add_layer(butterfly_layer)

    def update(self, delta_time):
        super().update(delta_time)
        self.physics_engine.update()
