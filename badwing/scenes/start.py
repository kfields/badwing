from crunge.engine.math import Bounds2
from crunge.engine.d2.physics import PhysicsEngine2D

from badwing.level import Level

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.characters.butterfly import Butterflies


class StartScene(Level):
    def __init__(self, name, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)

    def _create(self):
        super()._create()
        self.add_layer(BarrierLayer("barrier"))

        self.add_layer(
            BackgroundLayer(
                "background", ":resources:/backgrounds/backgroundColorGrass.png"
            )
        )
        self.butterfly_layer = butterfly_layer = SceneLayer("butterflies")
        #butterflies = Butterflies.create_random(20, self.bounds)
        butterflies = Butterflies.create_random(20)
        self.butterfly_layer.attach(butterflies)
        self.add_layer(butterfly_layer)
