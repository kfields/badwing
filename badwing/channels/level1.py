from crunge.engine.factory import ClassFactory
from crunge.engine.channel import SceneChannel

from ..badwing import BadWing
#from ..scenes.level1 import Level1
from ..level import TileLevel
from ..screens.level import LevelScreen


class Level1Channel(SceneChannel):
    def __init__(self):
        #super().__init__(ClassFactory(LevelScreen), ClassFactory(Level1), "level1", "Level 1")
        super().__init__(ClassFactory(LevelScreen), ClassFactory(TileLevel), "level1", "Level 1")

def install(app: BadWing):
    app.add_channel(Level1Channel())
