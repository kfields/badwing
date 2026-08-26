import glm

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D

class SceneView(SceneView2D):
    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2),
            2.0
        )
