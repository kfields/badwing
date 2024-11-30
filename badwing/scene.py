from crunge.engine.d2.physics_scene_2d import PhysicsScene2D
from crunge.engine.d2.physics import PhysicsEngine2D

import badwing.globe


class Scene(PhysicsScene2D):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(physics_engine)
        badwing.globe.scene = self
        self.name = name

        self.ground_layer = None
        self.paused = False
        '''
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
        '''

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def shutdown(self):
        pass
