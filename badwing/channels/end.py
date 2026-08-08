from crunge.engine.factory import ClassFactory

from crunge.engine.channel import PhysicsSceneChannel
from crunge.engine.d2.physics import PhysicsWorld2D

from ..badwing import BadWing
from ..scenes.end import EndScene
from ..screens.end_screen import EndScreen


class EndChannel(PhysicsSceneChannel):
    def __init__(self):
        super().__init__(
            ClassFactory(EndScreen),
            ClassFactory(EndScene),
            ClassFactory(PhysicsWorld2D),
            "end",
            "End",
        )


def install(app: BadWing):
    app.add_channel(EndChannel())
