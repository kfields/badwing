import glm

from crunge.engine.d2.scene_view_2d import SceneView2D
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

class SceneView(SceneView2D):
    def __init__(self, scene: Scene2D):
        super().__init__(scene)

    def _create(self):
        super()._create()
        self.scene.create()

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2),
            2.0
        )
