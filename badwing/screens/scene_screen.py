from loguru import logger

import glm

from crunge.engine.scheduler import Scheduler
from crunge.engine.math import Bounds2

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from ..scene_view import SceneView


class SceneScreen(SceneView):
    def __init__(self, scene: Level):
        super().__init__(scene)
        badwing.globe.screen = self
        self.controller_stack = []

    @property
    def controller(self):
        if not self.controller_stack:
            return None
        if len(self.controller_stack) == 0:
            return None
        return self.controller_stack[-1]

    def push_controller(self, controller):
        def callback(delta_time):
            self.controller_stack.append(controller)

        Scheduler().schedule_once(callback, 0)

    def pop_controller(self):
        def callback(delta_time):
            controller = self.controller_stack.pop()
            logger.debug(f"Popping controller: {controller}")
            #self.controller_stack[-1].reset()

        Scheduler().schedule_once(callback, 0)

    def on_size(self):
        super().on_size()
        '''
        bounds = self.bounds
        self.scene.bounds = Bounds2(bounds.left, bounds.bottom, bounds.right, bounds.top)
        '''
        self.recenter_camera()

    def recenter_camera(self):
        #bounds = self.bounds
        bounds = self.scene.bounds
        x = bounds.left + bounds.width / 2
        y = bounds.height / 2
        position = glm.vec2(x, y)
        logger.debug(f"Recentering camera to position: {position}")
        self.camera.position = position