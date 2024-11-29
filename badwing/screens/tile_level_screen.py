import glm

from badwing.constants import *

from ..level import TileLevel
from ..characters import Avatar

from .level_screen import LevelScreen


class TileLevelScreen(LevelScreen):
    scene: TileLevel
    def __init__(self, scene):
        super().__init__(scene)

    def _create(self):
        super()._create()

    def _post_create(self):
        super()._post_create()
        avatar = None
        for node in self.scene.character_layer.root.children:
            if isinstance(node, Avatar):
                avatar = node
                break
        self.push_avatar(avatar)

    def update(self, delta_time: float):
        # --- Manage Scrolling ---
        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.avatar.bounds.left < left_boundary:
            self.view_left -= left_boundary - self.avatar.bounds.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.avatar.bounds.right > right_boundary:
            self.view_left += self.avatar.bounds.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.avatar.bounds.top > top_boundary:
            self.view_bottom += self.avatar.bounds.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.avatar.bounds.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.avatar.bounds.bottom
            changed = True

        if changed:
            self.camera.position = glm.lerp(self.camera.position, self.avatar.position, delta_time)

        super().update(delta_time)
