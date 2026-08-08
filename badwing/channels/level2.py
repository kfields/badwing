from crunge.engine.factory import ClassFactory

from crunge.engine.channel import PhysicsSceneChannel
from crunge.engine.d2.physics import PhysicsWorld2D


from ..badwing import BadWing

from ..scenes.level2 import Level2
from ..screens.tile_level_screen import TileLevelScreen


class Level2Channel(PhysicsSceneChannel):
    def __init__(self):
        super().__init__(
            ClassFactory(TileLevelScreen),
            ClassFactory(Level2),
            ClassFactory(PhysicsWorld2D),
            "level2",
            "Level 2",
        )


def install(app: BadWing):
    app.add_channel(Level2Channel())
