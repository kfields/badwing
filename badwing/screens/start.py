from crunge import imgui

from crunge.engine import Renderer

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from ..scene_view import SceneView

class StartScreen(SceneView):
    def __init__(self, scene: Level):
        super().__init__(scene)
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

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
