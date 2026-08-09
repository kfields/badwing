from crunge.engine.factory import ClassFactory

from crunge.engine.channel import PhysicsSceneChannel
from crunge.engine.d2.physics import PhysicsWorld2D


from ..badwing import BadWing

from ..levels.cavern import CavernLevel
from ..screens.tile_level_screen import TileLevelScreen


class CavernChannel(PhysicsSceneChannel):
    def __init__(self, name: str, title: str, next_channel: str):
        super().__init__(
            ClassFactory(TileLevelScreen),
            ClassFactory(CavernLevel),
            ClassFactory(PhysicsWorld2D),
            name,
            title,
            next_channel,
        )


def install(app: BadWing):
    app.add_channels(
        [
            CavernChannel("cavern-1", "Cavern 1", "end"),
        ]
    )
