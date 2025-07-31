from loguru import logger

from crunge import imgui

from crunge.engine import Renderer, Scheduler
from crunge.engine.d2.physics.draw_options import DrawOptions

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from .scene_screen import SceneScreen

class LevelScreen(SceneScreen):
    def __init__(self, scene: Level):
        super().__init__(scene)
        self.avatar_stack = []

    def _create(self):
        super()._create()
        self.draw_options = DrawOptions(self.scratch)
    
    @property
    def avatar(self):
        return self.avatar_stack[-1]

    def push_avatar(self, avatar):
        self.avatar_stack.append(avatar)
        badwing.globe.avatar = avatar
        if avatar is not None:
            self.push_controller(avatar.control())

    def pop_avatar(self):
        self.avatar_stack.pop()
        avatar = self.avatar
        badwing.globe.avatar = avatar
        self.pop_controller()
        return avatar

    def draw(self, renderer: Renderer):
        imgui.begin("Main")

        imgui.text(f"Update time: {self.window.update_time:.3f}")
        imgui.text(f"Frame time: {self.window.frame_time:.3f}")

        _, self.debug_draw_enabled = imgui.checkbox("Debug Draw", self.debug_draw_enabled)

        if imgui.button("Quit"):
            #exit()
            Scheduler().schedule_once(lambda dt: exit(), 0)

        imgui.end()

        if self.debug_draw_enabled:
            self.scene.physics_engine.debug_draw(self.draw_options)

        super().draw(renderer)
