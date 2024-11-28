import json
import pymunk

from crunge.engine.d2.scene_2d import Scene2D
import badwing.globe
from badwing.constants import *
from badwing.assets import asset


class Scene(Scene2D):
    def __init__(self, name):
        super().__init__()
        badwing.globe.scene = self
        self.name = name

        self.debug_layer = None
        self.ground_layer = None
        self.paused = False
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
        self.controller_stack = []

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

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def shutdown(self):
        pass
