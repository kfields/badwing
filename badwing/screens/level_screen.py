from loguru import logger

from crunge import imgui

from crunge.engine import Scheduler
from crunge.engine.d2.physics.world_debug_overlay import WorldDebugOverlay

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from .scene_screen import SceneScreen

class LevelScreen(SceneScreen):
    def __init__(self, scene: Level):
        super().__init__(scene)
        self.avatar_stack = []
        self.show_beat_level_dialog = False

    def _create(self):
        super()._create()
        self.debug_layer = WorldDebugOverlay()
        self.add_overlay(self.debug_layer)

    @property
    def level(self) -> Level:
        return self.scene
    
    @property
    def avatar(self):
        return self.avatar_stack[-1]

    def push_avatar(self, avatar):
        if avatar is None:
            raise ValueError("Avatar cannot be None")
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

    def _draw(self):
        imgui.begin("Main")

        imgui.text(f"Update time: {self.window.update_time:.3f}")
        imgui.text(f"Frame time: {self.window.frame_time:.3f}")

        _, self.debug_layer.visible = imgui.checkbox(
            "Debug Draw", self.debug_layer.visible
        )
        

        if imgui.button("Restart"):
            badwing.globe.player.remove_level_progress(self.scene.name)
            badwing.globe.app.show_channel(self.scene.name)

        if imgui.button("Quit"):
            Scheduler().schedule_once(lambda dt: exit(), 0)

        if self.level.beaten:
            imgui.open_popup("Level Complete")

        if imgui.begin_popup_modal("Level Complete", True)[0]:
            imgui.text("Proceed to the next level:")
            if imgui.button("OK"):
                badwing.globe.app.show_channel(self.level.next_level)
                imgui.close_current_popup()
            imgui.end_popup()

        imgui.end()

        super()._draw()
