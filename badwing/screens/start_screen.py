import sys
import os

from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.math import Bounds2
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.scene_view_2d import SceneView2D

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level
from badwing.controller import Controller

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.characters.butterfly import Butterflies


class StartScreen(SceneView2D):
    def __init__(self):
        super().__init__('start')
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    @classmethod
    def produce(self):
        level = StartScreen()
        return level

    def _create(self):
        super()._create()
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def draw(self, renderer: Renderer):
        imgui.begin("Main")

        if imgui.button("Start"):
            badwing.globe.game.show_channel("level1")

        if imgui.button("Quit"):
            exit()

        imgui.end()
        super().draw(renderer)
