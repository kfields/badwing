from crunge.engine.d2.physics import PhysicsWorld2D

import badwing.globe
from badwing.constants import *
from badwing.scene import Scene

from ..map.map_loader import MapLoader

from badwing.player.player import LevelProgress


class Level(Scene):
    def __init__(self, name: str, physics_engine: PhysicsWorld2D):
        super().__init__(name, physics_engine)
        badwing.globe.scene = self

    def _create(self):
        super()._create()
        tmx_path = f":resources:/{self.name}.tmx"
        map_loader = MapLoader(self)
        map_loader.load(tmx_path)

    def create_progress(self):
        return LevelProgress(self.name)

    def update(self, delta_time):
        super().update(delta_time)

        if not self.paused:
            self.physics_engine.update(1 / 60)
            self.check_collisions()

    def check_collisions(self):
        pass
