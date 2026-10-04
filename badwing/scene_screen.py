from loguru import logger
import glm

from crunge.engine.d2.screen import SceneScreen2D
from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

from crunge.engine.scheduler import Scheduler

import badwing.globe

from .scene_view import SceneView


class SceneScreen(SceneScreen2D):
    view: SceneView

    def __init__(self, scene: Scene2D, name: str = "SceneScreen", title: str = "Scene Screen"):
        super().__init__(scene, name=name, title=title)
        badwing.globe.screen = self

    def create_views(self):
        logger.debug("Creating screen views")
        self.view = SceneView(self.scene)
        self.add_child(self.view)

    @property
    def ppu(self) -> float:
        return self.camera.ppu

    @property
    def camera(self) -> Camera2D:
        return self.view.camera

    def on_size(self):
        super().on_size()
        self.recenter_camera()

    def recenter_camera(self):
        # bounds = self.bounds
        bounds = self.scene.bounds
        x = bounds.left + bounds.width / 2
        y = bounds.height / 2
        position = glm.vec2(x, y)
        logger.debug(f"Recentering camera to position: {position}")
        self.camera.position = position
