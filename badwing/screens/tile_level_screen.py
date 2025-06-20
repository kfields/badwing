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
        for node in self.scene.character_layer.root.children:
            if isinstance(node, Avatar):
                avatar = node
                break
        self.push_avatar(avatar)

    def update(self, delta_time: float):
        if self.avatar is None:
            return
        # --- Manage Scrolling ---
        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.avatar.bounds.left < left_boundary:
            self.view_left -= left_boundary - self.avatar.bounds.left
            changed = True

        # Scroll right
        #right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        right_boundary = self.view_left + self.width - RIGHT_VIEWPORT_MARGIN
        if self.avatar.bounds.right > right_boundary:
            self.view_left += self.avatar.bounds.right - right_boundary
            changed = True

        # Scroll up
        #top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        top_boundary = self.view_bottom + self.height - TOP_VIEWPORT_MARGIN
        if self.avatar.bounds.top > top_boundary:
            self.view_bottom += self.avatar.bounds.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.avatar.bounds.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.avatar.bounds.bottom
            changed = True

        if changed:
            velocity = self.avatar.velocity
            speed = glm.length(velocity) / 256
            #speed = glm.length(velocity) / 128

            #logger.debug(f"delta_time: {delta_time}")
            #logger.debug(f"velocity: {velocity}")
            #logger.debug(f"speed: {speed}")

            frustrum = self.camera.frustrum

            # Compute clamping limits to keep the frustum inside level bounds
            min_x = self.scene.bounds.min.x + (frustrum.max.x - frustrum.min.x) / 2
            max_x = self.scene.bounds.max.x - (frustrum.max.x - frustrum.min.x) / 2
            min_y = self.scene.bounds.min.y + (frustrum.min.y - frustrum.max.y) / 2
            max_y = self.scene.bounds.max.y - (frustrum.min.y - frustrum.max.y) / 2

            #min_y = max(self.scene.bounds.min.y, min_y)
            # TODO: Hack.
            #min_y = min_y + frustrum.height - 128
            min_y = min_y + frustrum.height
            #max_y = min(self.scene.bounds.max.y, max_y)
            #max_y = max_y + frustrum.height

            #logger.debug(f"scene bounds: {self.scene.bounds}")
            #logger.debug(f"frustrum: {frustrum}")
            #logger.debug(f"min_x: {min_x}")
            #logger.debug(f"max_x: {max_x}")
            #logger.debug(f"min_y: {min_y}")
            #logger.debug(f"max_y: {max_y}")

            camera_position = glm.mix(self.camera.position, self.avatar.position, speed * delta_time)
            camera_x = glm.clamp(camera_position.x, min_x, max_x)
            camera_y = glm.clamp(camera_position.y, min_y, max_y)
            self.camera.position = glm.vec2(camera_x, camera_y)

        super().update(delta_time)
