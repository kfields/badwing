from loguru import logger
import glm

from badwing.constants import *

from ..level import TileLevel
from ..characters import Avatar

from .level_screen import LevelScreen


class TileLevelScreen(LevelScreen):
    scene: TileLevel
    def __init__(self, scene):
        super().__init__(scene)
        self.debug_draw_enabled = False

    def _create(self):
        super()._create()
        avatar = None
        logger.debug(f"Character layer children: {self.scene.character_layer.root.children}")
        for node in self.scene.character_layer.root.children:
            logger.debug(f"Checking node: {node}")
            if isinstance(node, Avatar):
                avatar = node
                break
        self.push_avatar(avatar)
        self.update_camera()

    def recenter_camera(self):
        if self.avatar is None:
            return
        self.camera.position = self.avatar.position
        self.update_camera()
        
    def update(self, delta_time: float):
        self.update_camera(delta_time)
        super().update(delta_time)

    def update_camera(self, delta_time: float = 1/60):
        if self.avatar is None:
            return
        velocity = self.avatar.velocity
        speed = glm.length(velocity) / 128

        #logger.debug(f"delta_time: {delta_time}")
        #logger.debug(f"velocity: {velocity}")
        #logger.debug(f"speed: {speed}")

        frustum = self.camera.frustum

        # Compute clamping limits to keep the frustum inside level bounds
        min_x = self.scene.bounds.min.x + (frustum.max.x - frustum.min.x) / 2
        max_x = self.scene.bounds.max.x - (frustum.max.x - frustum.min.x) / 2
        min_y = self.scene.bounds.min.y + (frustum.min.y - frustum.max.y) / 2
        max_y = self.scene.bounds.max.y - (frustum.min.y - frustum.max.y) / 2

        #min_y = max(self.scene.bounds.min.y, min_y)
        # TODO: Hack.
        min_y = min_y + frustum.height

        #logger.debug(f"scene bounds: {self.scene.bounds}")
        #logger.debug(f"frustum: {frustum}")
        #logger.debug(f"min_x: {min_x}")
        #logger.debug(f"max_x: {max_x}")
        #logger.debug(f"min_y: {min_y}")
        #logger.debug(f"max_y: {max_y}")

        camera_position = glm.mix(self.camera.position, self.avatar.position, speed * delta_time)
        camera_x = glm.clamp(camera_position.x, min_x, max_x)
        camera_y = glm.clamp(camera_position.y, min_y, max_y)
        self.camera.position = glm.vec2(camera_x, camera_y)
