from crunge import imgui

from crunge.engine import Renderer, Scheduler

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from .scene_screen import SceneScreen

class StartScreen(SceneScreen):
    def __init__(self, scene: Level):
        super().__init__(scene)

    def _draw(self):
        imgui.begin("Main")

        if imgui.button("Start"):
            badwing.globe.game.show_channel("level1")

        if imgui.button("Quit"):
            Scheduler().schedule_once(lambda dt: exit(), 0)

        imgui.end()
        super()._draw()
