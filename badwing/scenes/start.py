from typing import List
from loguru import logger

from crunge.engine.math import Bounds2
from crunge.engine.d2.physics import PhysicsEngine2D
from crunge.engine.d2.scene.layer import GraphLayer2D

from badwing.level import Level

from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.characters.butterfly import Butterfly, Butterflies


class StartScene(Level):
    def __init__(self, name, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)
        self.butterflies: List[Butterfly] = []

    def _create(self):
        super()._create()
        self.add_layer(BarrierLayer("barrier"))

        self.add_layer(
            BackgroundLayer(
                "background", ":resources:/backgrounds/backgroundColorGrass.png"
            )
        )
        self.butterfly_layer = butterfly_layer = GraphLayer2D("butterflies")

        bounds = Bounds2(self.bounds.left, self.bounds.bottom, self.bounds.right, self.bounds.top)
        logger.debug(f"Creating butterflies within bounds: {bounds}")

        self.butterflies = Butterflies.create_random(20, bounds)
        #butterflies = Butterflies.create_random(20)
        self.butterfly_layer.attach(self.butterflies)
        self.add_layer(butterfly_layer)
