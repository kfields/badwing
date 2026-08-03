from crunge.engine.factory import ClassFactory

from crunge.engine.channel import PhysicsSceneChannel
from crunge.engine.d2.physics import PhysicsWorld2D


from ..badwing import BadWing

from ..scenes.level1 import Level1
from ..screens.tile_level_screen import TileLevelScreen


class Level1Channel(PhysicsSceneChannel):
    def __init__(self):
        super().__init__(
            ClassFactory(TileLevelScreen),
            ClassFactory(Level1),
            ClassFactory(PhysicsWorld2D),
            "level1",
            "Level 1",
        )


def install(app: BadWing):
    app.add_channel(Level1Channel())
