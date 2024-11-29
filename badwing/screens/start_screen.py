from crunge import imgui

from crunge.engine import Renderer

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from .scene_screen import SceneScreen

class StartScreen(SceneScreen):
    def __init__(self, scene: Level):
        super().__init__(scene)

    def _create(self):
        super()._create()

    def draw(self, renderer: Renderer):
        imgui.begin("Main")

        if imgui.button("Start"):
            badwing.globe.game.show_channel("level1")

        if imgui.button("Quit"):
            exit()

        imgui.end()
        super().draw(renderer)
