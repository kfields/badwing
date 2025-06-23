from loguru import logger

from crunge.engine.scheduler import Scheduler

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
