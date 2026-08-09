from crunge.engine.factory import ClassFactory

from crunge.engine.channel import PhysicsSceneChannel
from crunge.engine.d2.physics import PhysicsWorld2D


from ..badwing import BadWing

from ..levels.playground import PlaygroundLevel
from ..screens.tile_level_screen import TileLevelScreen


class PlaygroundChannel(PhysicsSceneChannel):
    def __init__(self, name: str, title: str, next_channel: str):
        super().__init__(
            ClassFactory(TileLevelScreen),
            ClassFactory(PlaygroundLevel),
            ClassFactory(PhysicsWorld2D),
            name,
            title,
            next_channel,
        )


def install(app: BadWing):
    app.add_channels(
        [
            #PlaygroundChannel("playground-1", "Playground 1", "playground-2"),
            PlaygroundChannel("playground-1", "Playground 1", "cavern-1"),
            #PlaygroundChannel("playground-2", "Playground 2", "cavern-1"),
        ]
    )
