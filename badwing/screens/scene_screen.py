from crunge import imgui

from crunge.engine import Renderer

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from ..scene_view import SceneView

class SceneScreen(SceneView):
    def __init__(self, scene: Level):
        super().__init__(scene)
        badwing.globe.screen = self
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.controller_stack = []

    def _create(self):
        super()._create()
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    @property
    def controller(self):
        if not self.controller_stack:
            return None
        if len(self.controller_stack) == 0:
            return None
        return self.controller_stack[-1]

    def push_controller(self, controller):
        self.controller_stack.append(controller)
        badwing.globe.controller = controller

    def pop_controller(self):
        controller = self.controller_stack.pop()
        badwing.globe.controller = controller
        return controller
