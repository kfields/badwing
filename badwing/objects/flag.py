from badwing.player.player import Player
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import SpriteVu

from ..collectible import Collectible


class Pole(Node2D, Collectible):
    def __init__(self, position, sprite):
        super().__init__(position, vu=SpriteVu(), model=sprite)
        self.collected = False

    def on_collect(self, player: Player) -> bool:
        return False


class Flag(Node2D, Collectible):
    stage = 0

    def __init__(self, position, sprite):
        super().__init__(position, vu=SpriteVu(), model=sprite)
        self.collected = False

    @classmethod
    def produce(self, kind, position, sprite):
        node = kinds[kind].produce(position, sprite)
        return node

    def on_collect(self, player):
        progress = player.level_progress
        if progress.stage != self.stage - 1:
            return False   # out of order, or already taken
        progress.stage = self.stage
        return True
    
    '''
    def on_collect(self, player: Player) -> bool:
        self.collected = True
        return True
    '''

class FlagGreen(Flag):
    stage = 1
    @classmethod
    def produce(self, position, sprite):
        return FlagGreen(position, sprite)


class FlagYellow(Flag):
    stage = 2
    @classmethod
    def produce(self, position, sprite):
        return FlagYellow(position, sprite)


class FlagRed(Flag):
    stage = 3
    @classmethod
    def produce(self, position, sprite):
        return FlagRed(position, sprite)


kinds = {
    "Pole": Pole,
    "FlagGreen": FlagGreen,
    "FlagYellow": FlagYellow,
    "FlagRed": FlagRed,
}
