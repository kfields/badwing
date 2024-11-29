from crunge import imgui

from crunge.engine import Renderer

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from .scene_screen import SceneScreen

class LevelScreen(SceneScreen):
    def __init__(self, scene: Level):
        super().__init__(scene)
        self.avatar_stack = []

    @property
    def avatar(self):
        return self.avatar_stack[-1]

    def push_avatar(self, avatar):
        self.avatar_stack.append(avatar)
        badwing.globe.avatar = avatar
        self.push_controller(avatar.control())

    def pop_avatar(self):
        avatar = self.avatar_stack.pop()
        badwing.globe.avatar = avatar
        self.pop_controller()
        return avatar

    def draw(self, renderer: Renderer):
        imgui.begin("Main")

        if imgui.button("Start"):
            badwing.globe.game.show_channel("level1")

        if imgui.button("Quit"):
            exit()

        imgui.end()
        super().draw(renderer)
