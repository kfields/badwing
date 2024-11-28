import glm

from crunge.engine import Renderer
from crunge.engine.d2.scene_view_2d import SceneView2D
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

class SceneView(SceneView2D):
    def __init__(self, scene: Scene2D):
        super().__init__(scene)

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2),
            glm.vec2(self.width, self.height),
            2.0
        )

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_2d=self.camera)

    '''
    def draw(self, renderer: Renderer):
        with self.renderer:
            #self.scene.draw(self.renderer)
            super().draw(self.renderer)
    '''
    
    '''
    def open(self):
        self.ui_manager.enable()
        self.create()

    def close(self):
        self.ui_manager.disable()
    '''