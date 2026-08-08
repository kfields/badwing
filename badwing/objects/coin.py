import glm

from crunge.engine.d2.node_2d import Node2D
from ..player import Player

from badwing.constants import *

from ..collectible import Collectible


class Coin(Node2D, Collectible):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position, sprite):
        kind = sprite.properties['class']
        node = kinds[kind].produce(position, sprite)
        return node

    def on_collect(self, player: Player) -> None:
        pass


class Gem(Coin, Collectible):
    def __init__(self, position=glm.vec2(), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position=glm.vec2(), sprite=None):
        return Gem(position, sprite)

    def on_collect(self, player: Player) -> None:
        pass

kinds = {
    'coin': Gem
}
