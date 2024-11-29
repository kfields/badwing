from crunge.engine.factory import ClassFactory
from crunge.engine.channel import SceneChannel

from ..badwing import BadWing
from ..scenes.start import StartScene
from ..screens.start_screen import StartScreen


class StartChannel(SceneChannel):
    def __init__(self):
        super().__init__(ClassFactory(StartScreen), ClassFactory(StartScene), "start", "Start")

def install(app: BadWing):
    app.add_channel(StartChannel())
